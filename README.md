# RuneLite Wrapped
![banner](/assets/runelite_wrapped_icon_wide.png)


## Basic Architecture

![Architecture Graph](/assets/runelite_wrapped_architecture.svg)


## Components

* [Plugin](/src/plugin/README.md)
  * A plugin for RuneLite that sends game data to the ingestor service.
  * Users will need to have this plugin installed in their local RuneLite for us to receive their game data.
* [Ingestor](/src/ingestor/README.md)
  * This is an API that receives the data (via HTTP POST) from the plugin and stores it in a mongoDB instance
* [Analytics](/src/analytics/README.md)
  * This is a collection of data processing pipelines running in a [dagster](https://dagster.io/) instance
  * These pipelines turn the raw game telemetry into useful stats for the Wrapped report
* [Webapp](/src/webapp/README.md)
  * This is the Web App that users will go to to see their Wrapped report

## Relevant Tutorials

I have linked a bunch of relevant tutorials for spooling up [here](/tutorials/)
