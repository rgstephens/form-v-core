# Forms vs Core - Rasa X Demo Bot

Example bot showing the differences between implementing the same story with forms vs. featurized slots.

One aspect of this test is that we want the bot stories to take into account slots that are already
set within the session. We will NOT reset slots between stories.

Example dialog with forms:

```
> beer form
what beer style do you like
> ale
what type of beer do you like
> brown
you might like a Newcastle Brown Ale
> how's the weather
Sorry, I don't recognize that question, want to try again?
> give me a form based beer suggestion
you might like a Newcastle Brown Ale
> i like amber
```

Example dialog with featurized slots:

```
> beer core
...
```

Admin intents:

- show slots
- clear slots
- f1 scores
- version

# Running the Demo

The chatbot is setup to run under the lighterweight local Rasa X install in a Docker container with `docker-compose`.

Update the version numbers in the `.env` file. You can find the version info in the tags for the [Docker Hub Images](https://hub.docker.com/u/rasa).

```
RASA_X_VERSION=0.25.1
RASA_VERSION=1.7.0
RASA_SDK_VERSION=1.7.0
```

You can run your own copy of the bot using these steps:

```sh
git clone https://github.com/rgstephens/form-v-core.git
cd form-v-core
docker-compose build --no-cache
docker-compose run rasa rasa train
docker-compose up -d
docker-compose logs rasa | grep password
```

## Ports

The `docker-compose.yml` uses the default ports which can be over-ridden. This is partcularly useful if you want to run multiple chatbots on the same host.

- `5005` - Rasa port (point your client here)
- `5002` - Rasa X UI

## Update Server

To update the server, update the version numbers in the `.env` and enter the following commands

```sh
sudo docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

# Training

Local training using your local python environment (or conda/venv)

```sh
docker-compose run rasa rasa train
```

# Testing

After training the model, run the command:

```sh
docker-compose run rasa rasa test nlu -u test/test_data.md --model models/$(ls models)
docker-compose run rasa rasa test core --stories test/test_stories.md
```

# Rasa Interactive Shell

```sh
docker run -v $(pwd):/app rasa/rasa:${RASA_VERSION} run actions --actions actions.actions
docker-compose up app -d
docker run -it -v $(pwd):/app rasa/rasa:${RASA_VERSION} shell --debug
```

With Docker:

```sh
export RASA_X_VERSION=1.5.1-full
export RASA_MODEL_SERVER="https://localhost:5002"
docker run --it --rm --network=$(basename `pwd`)_default -v $(pwd):/app rasa/rasa:${RASA_X_VERSION} shell --model /app/models/$(ls models) --endpoints endpoints_local.yml
```

# Scripts

The project includes the following scripts:

| Script              | Usage                              |
| ------------------- | ---------------------------------- |
| entrypoint.sh       | Docker entrypoint for full Rasa X  |
| entrypoint_local.sh | Docker entrypoint for local Rasa X |

# Rasa X & Rasa Version Combinations

The docker repo tags page will show you the latest versions.

* [Rasa X Docker Hub Tags](https://hub.docker.com/r/rasa/rasa-x/tags)
* [Rasa Docker Hub Tags](https://hub.docker.com/r/rasa/rasa/tags)
* [Rasa SDK Docker Hub Tags](https://hub.docker.com/r/rasa/rasa-sdk/tags)

| Rasa X |  Rasa  | Rasa SDK |
| :----: | :----: | :------: |
| 0.25.1 | 1.7.1  |  1.7.0   |
| 0.24.6 | 1.6.1  |  1.6.1   |
| 0.23.5 | 1.5.3  |  1.5.2   |
| 0.23.3 | 1.5.1  |  1.5.0   |
| 0.22.1 | 1.4.3  |  1.4.0   |
| 0.21.5 | 1.3.9  |  1.3.3   |
| 0.21.4 | 1.3.9  |  1.3.3   |
| 0.21.3 | 1.3.9  |  1.3.3   |
| 0.20.5 | 1.2.11 |  1.2.0   |
| 0.20.0 | 1.2.5  |  1.2.0   |
