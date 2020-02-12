## suggest_beer_form
* suggest_beer_form
  - beer_suggestion_form
  - form{"name": "beer_suggestion_form"}
  - form{"name": null}

## suggest_beer_form
* suggest_beer_form
  - beer_suggestion_form
  - form{"name": "beer_suggestion_form"}
  - slot{"requested_slot": "beer_type"}
* inform{"beer_type":"ale"}
  - slot{"beer_type":"ale"}
  - slot{"requested_slot": "beer_style"}
* inform{"beer_style":"brown"}
  - slot{"beer_style":"brown"}
  - form{"name": null}

## suggest_beer_core empty - ale, brown
* suggest_beer_core
  - action_set_slots
  - utter_ask_beer_type
* inform{"beer_type":"ale"}
  - slot{"beer_type":"ale"}
  - utter_ask_beer_style
* inform{"beer_style":"brown"}
  - slot{"beer_style":"brown"}
  - utter_ale_brown

## suggest_beer_core ale brown
* suggest_beer_core
  - action_set_slots
  - slot{"beer_type":"ale"}
  - slot{"beer_style":"brown"}
  - utter_ale_brown

## suggest_beer_core ale amber
* suggest_beer_core
  - action_set_slots
  - slot{"beer_type":"ale"}
  - slot{"beer_style":"amber"}
  - utter_ale_amber

## suggest_beer_core_noslots ale brown
* suggest_beer_core_noslots
  - slot{"beer_type":"ale"}
  - slot{"beer_style":"brown"}
  - utter_ale_brown

## story_greet <!--- The name of the story. It is not mandatory, but useful for debugging. -->
* greet <!--- User input expressed as intent. In this case it represents users message 'Hello'. -->
  - utter_greet <!--- The response of the chatbot expressed as an action. In this case it represents chatbot's response 'Hello, how can I help?' -->

## greet 2
* greet
  - utter_greet
* goodbye
  - utter_goodbye
  - action_restart

## inform 
* inform
  - utter_slots

## inform beer_type
* inform{"beer_type":"ale"}
  - slot{"beer_type":"ale"}
  - utter_slots

## inform beer_style
* inform{"beer_style":"brown"}
  - slot{"beer_style":"brown"}
  - utter_slots

## story_goodbye
* goodbye
  - utter_goodbye
  - action_restart

## clear
* clear
  - utter_slots
  - utter_clear
  - utter_slots
  - action_restart

## f1_score
* f1_score
  - action_f1_score

## story_thanks
* thanks
  - utter_thanks

## version
* version
  - utter_version
  - action_version

## chitchat #1
* chitchat
  - utter_chitchat

## show slot 1
* show_slots
  - utter_slots
