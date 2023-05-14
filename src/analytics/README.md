# Runelite Wrapped Analytics

This is a collection of dagster assets that should run ETL (extract, transform, load) pipelines to calculate all stats needed for the wrapped slideshow for each user.

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
