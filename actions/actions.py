# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from typing import Dict, Text, Any, List, Union, Type, Optional

import typing
import logging
import requests
import json
import csv

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_sdk.executor import CollectingDispatcher

#from rasa_core.trackers import (
#    DialogueStateTracker, ActionExecuted,
#    EventVerbosity)
#from rasa_core.policies.fallback import FallbackPolicy
#from rasa_core.domain import Domain
from datetime import datetime, date, time
#from rasa_core.utils import AvailableEndpoints
#from rasa_core.tracker_store import TrackerStore

logger = logging.getLogger(__name__)
vers = 'Vers: 0.7.0, Date: Mar 18, 2019'


def get_last_event_for(tracker, event_type: Text, action_names_to_exclude: List[Text] = None, skip: int = 0) -> Optional[Any]:
    """Gets the last event of a given type which was actually applied.

    Args:
        event_type: The type of event you want to find.
        action_names_to_exclude: Events of type `ActionExecuted` which
            should be excluded from the results. Can be used to skip
            `action_listen` events.
        skip: Skips n possible results before return an event.

    Returns:
        event which matched the query or `None` if no event matched.
    """
    #import copy
    #to_exclude = action_names_to_exclude or []

    def filter_function(e):
        #logger.debug("e: {}".format(e))
        #logger.debug("e.event: {}".format(e["event"]))
        has_instance = e
        if e["event"] == event_type:
            has_instance = e
            #logger.debug("  filtering event, intent name: {}".format(has_instance["parse_data"]["intent"]["name"]))
        #excluded = (isinstance(e, ActionExecuted) and e.action_name in to_exclude)
        excluded = (e["event"] != event_type or ((e["event"] == event_type and ((e["parse_data"]["intent"]["name"] == "domicile") or (e["parse_data"]["intent"]["name"] == "customertype")))))

        return has_instance and not excluded

    filtered = filter(filter_function, reversed(tracker.events))
    for i in range(skip):
        next(filtered, None)

    return next(filtered, None)

def intentHistoryStr(tracker, skip, past):
    msg = ""
    prev_user_event = get_last_event_for(tracker, 'user', skip=skip)
    logger.info("event.text: {}, intent: {}, confidence: {}".format(prev_user_event["text"], prev_user_event["parse_data"]["intent"]["name"], prev_user_event["parse_data"]["intent"]["confidence"]))
    msg = "Ranked F1 scores:\n"
    msg += "* " + prev_user_event["parse_data"]["intent"]["name"] + " (" + "{:.4f}".format(prev_user_event["parse_data"]["intent"]["confidence"]) + ")\n"
    for i in range(past - 1):
        msg += "* " + prev_user_event["parse_data"]["intent_ranking"][i+1]["name"] + " (" + "{:.4f}".format(prev_user_event["parse_data"]["intent_ranking"][i+1]["confidence"]) + ")\n"
    return msg
    #msg += "* " + prev_user_event["parse_data"]["intent_ranking"][2]["name"] + " (" + "{:.4f}".format(prev_user_event["parse_data"]["intent_ranking"][2]["confidence"]) + ")\n"
    #msg += "* " + prev_user_event["parse_data"]["intent_ranking"][3]["name"] + " (" + "{:.4f}".format(prev_user_event["parse_data"]["intent_ranking"][3]["confidence"]) + ")"

def log_slots(tracker):
    #import copy
    # Log currently set slots
    logger.debug("tracker now has {} events".format(len(tracker.events)))
    prev_user_event = get_last_event_for(tracker, 'user', skip=1)
    logger.debug("event.text: {}, intent: {}, confidence: {}".format(prev_user_event["text"], prev_user_event["parse_data"]["intent"]["name"], prev_user_event["parse_data"]["intent"]["confidence"]))
    feedback_answer = tracker.get_slot("feedback")
    logger.debug("feedback: {}".format(feedback_answer))

class ActionF1Score(Action):
    def name(self):
        return "action_f1_score"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        msg = intentHistoryStr(tracker, 1, 4)
        dispatcher.utter_message(msg) #send the message back to the user
        return []

class ActionVersion(Action):
    def name(self):
        logger.info("ActionVersion self called")
        # define the name of the action which can then be included in training stories
        return "action_version"

    def run(self, dispatcher, tracker, domain):
        #logger.info(">>> responding with version: {}".format(vers))
        #dispatcher.utter_message(vers) #send the message back to the user
        request = json.loads(requests.get('http://rasa-x:5002/api/version').text)
        logger.info(">> rasa x version response: {}".format(request['rasa-x']))
        logger.info(">> rasa version response: {}".format(request['rasa']['production']))
        dispatcher.utter_message(f"Rasa X: {request['rasa-x']}\nRasa:  {request['rasa']['production']}")
        return []

class ActionSetSlots(Action):
    def name(self):
        logger.error("ActionSetSlots self called")
        return "action_set_slots"

    def slot_mappings(self):
        return {
            "beer_type": self.from_entity(entity="beer_type"),
            "beer_style": self.from_entity(entity="beer_style"),
        }

    def run(self, dispatcher, tracker, domain):
        beer_type = tracker.get_slot('beer_type')
        beer_style = tracker.get_slot('beer_style')
        return [SlotSet("beer_type", beer_type), SlotSet("beer_style", beer_style)]


class BeerSuggestionForm(FormAction):
    """Collects sales information and adds it to the spreadsheet"""

    def name(self):
        return "beer_suggestion_form"

    @staticmethod
    def required_slots(tracker):
        logger.error("required_slots")
        return [
            "beer_type",
            "beer_style",
        ]

    def slot_mappings(self):
        logger.error("slot_mappings")
        return {
            "beer_type": self.from_entity(entity="beer_type"),
            "beer_style": self.from_entity(entity="beer_style"),
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        logger.error("submit")
        beer_type = tracker.get_slot("beer_type")
        beer_style = tracker.get_slot("beer_style")

        dispatcher.utter_template("utter_" + beer_type + "_" + beer_style, tracker)
        return []
