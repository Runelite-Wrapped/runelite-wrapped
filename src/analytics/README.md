# Runelite Wrapped Analytics

This is a collection of dagster assets that should run ETL (extract, transform, load) pipelines to calculate all stats needed for the wrapped slideshow for each user.

## Overview

Here are some bullet points highlighting important things to know about this part of the project

* The Analytics engine converts raw game telemetry from the plugin and produces meaningful statistic to put into a Wrapped report
* It will read data from the mongoDB instance (that has data populated from by the ingestor), calculate statistics based of that, and store those new statistics back in the database (in a different collection/database to the raw game data)
* I imagine an example of these stats would be things like "total game play", where a pipeline might run a query against the mongo db to produce the total number of gameticks recorded and multiply it by 0.6 to get total seconds in game.
  * Another more complicated example might be "Most killed mob"
* We are going to use dagster as the workflow orchestrator (basically a fancy cron server with a UI and logs) to run these pipelines
  * Mainly because it would be cool to learn, and is pretty helpful for managing data projects in a team.
* We will eventually target a kubernetes deployment of dagster, but for now running it locally to test should suffice.

## Setup

You'll need a dagster instance (can be just running it locally for development)

## Pipeline Overview

Each pipeline should have three well defined sections
* Extract
* Transform
* Load

These can be separated into different python functions, or they could be completely different pipelines/assets in dagster.

In the extract step:
* Extract data from the raw data mongodb instance, into ram (i.e. just store it as a variable in python)
    * example: extract all the "actor-death" events for user "shupwup"
* Transform the data, I.e. calculate something from the data you
    * example: count the total number of deaths
* Load your processed data back into the mongo instance
    * example: store your death count in a new mongodb "collection" with some metadata like `"calculated_date"` or something.

## Early DAG Ideas

* Stat calculation for individual users
* Building the Stat -> image map (i.e. what image to display for each mob in the "Most killed mob" stat)
* OSRS Hiscores scraping



# Dagster Docs:

This is a [Dagster](https://dagster.io/) project scaffolded with [`dagster project scaffold`](https://docs.dagster.io/getting-started/create-new-project).

## Getting started

First, install your Dagster code location as a Python package. By using the --editable flag, pip will install your Python package in ["editable mode"](https://pip.pypa.io/en/latest/topics/local-project-installs/#editable-installs) so that as you develop, local code changes will automatically apply.

```bash
pip install -e ".[dev]"
```

Then, start the Dagster UI web server:

```bash
dagster dev
```

Open http://localhost:3000 with your browser to see the project.

You can start writing assets in `analytics/assets.py`. The assets are automatically loaded into the Dagster code location as you define them.

## Development


### Adding new Python dependencies

You can specify new Python dependencies in `setup.py`.

### Unit testing

Tests are in the `analytics_tests` directory and you can run tests using `pytest`:

```bash
pytest analytics_tests
```

### Schedules and sensors

If you want to enable Dagster [Schedules](https://docs.dagster.io/concepts/partitions-schedules-sensors/schedules) or [Sensors](https://docs.dagster.io/concepts/partitions-schedules-sensors/sensors) for your jobs, the [Dagster Daemon](https://docs.dagster.io/deployment/dagster-daemon) process must be running. This is done automatically when you run `dagster dev`.

Once your Dagster Daemon is running, you can start turning on schedules and sensors for your jobs.

## Deploy on Dagster Cloud

The easiest way to deploy your Dagster project is to use Dagster Cloud.

Check out the [Dagster Cloud Documentation](https://docs.dagster.cloud) to learn more.
