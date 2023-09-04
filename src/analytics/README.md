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


## Early DAG Ideas

* Stat calculation for individual users
* Building the Stat -> image map (i.e. what image to display for each mob in the "Most killed mob" stat)
* OSRS Hiscores scraping
