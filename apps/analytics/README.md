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

### A note about Dagster

Dagster is a python framework that helps us run data processing pipelines (just think a bunch of python functions that run in a specific order) on one or many machines.

Let's look at an example of how Dagster can help us - Let's say we want our Wrapped reports to update daily.

So maybe we write a python function that pulls a players data from our mongoDB instance, calculates the report stats, and pushes it back to a different part of the db. We could write our own script to run that every evening - not too hard right? But we would quickly run into some issues that dagster will solve for us:

* Visibility
  * We will want easily accessible live updates from pipeline runs
* Managing complexity of pipelines
  * We might later decide that we also need to calculate some auxiliary stats for each user, and then add a feature for aggregating stats for an entire clan chat
  * Dagster will handle the growing pipeline complexity, and provide convenient abstractions that scale well
* Configuration for specific runs
  * What if we decide we want to re-run a pipeline for a specific set of users?
  * Dagster allows for configuring runs in it's web UI, providing great flexibility
* Scheduling jobs - what should we run next? what can run in parallel?
  * When using Dagsters abstractions (assets, jobs, resources, io managers, etc) we no longer need to worry about the order in which pipelines run
  * Dagster will figure out if a specific task (i.e. one of many functions in a pipeline) has everything it needs to run.
  * If multiple pipelines have everything they need, dagster will run them in parallel for us
* Distributing compute over many machines
  * When our jobs get bigger, we might need to distribute data processing across many machines
  * In our case, this will be a good problem to have (it means we'll have many users!)

## Setup

The setup is pretty ad hoc at this point. You should have a virtual environment at the root of your repository, this assumes that you have already set that up and activated it (see the [root README](/README.md) for more info).

### Setting up dagster locally

This is for linux, I recommend setting up WSL2 for Windows users.

```bash
# From the root of the repository
pip install -r apps/analytics/requirements.txt
```

## Running

With the virtual environment activated you can run:

```bash
dagster dev -m analytics
```

And a local dagster instance will be spooled up, accessible by default from `localhost:3000` in your browser.

Note you will need to have the MONGO_URI environment variable set, pointing to the mongoDB instance you want to read from and write to.

For development I recommend setting up a local mongoDB instance using docker, and setting the MONGO_URI to `mongodb://localhost:27017/`.

I have a data dump from our dev mongoDB instance that I can share with you to set up your local instance with some test data.

## Early DAG Ideas

* Stat calculation for individual users
* Building the Stat -> image map (i.e. what image to display for each mob in the "Most killed mob" stat)
* OSRS Hiscores scraping
