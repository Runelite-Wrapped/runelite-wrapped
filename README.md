# RuneLite Wrapped
![banner](/assets/runelite_wrapped_icon_wide.png)


## Basic App Architecture

![Architecture Graph](/assets/runelite_wrapped_architecture.svg)

## Components

* [Plugin](/apps/plugin/README.md)
  * A plugin for RuneLite that sends game data to the ingestor service.
  * Users will need to have this plugin installed in their local RuneLite for us to receive their game data.
  * Written in Java
* [Ingestor](/apps/ingestor/README.md)
  * This is an API that receives the data (via HTTP POST) from the plugin and stores it in a mongoDB instance
  * Written in Python
* [Analytics](/apps/analytics/README.md)
  * This is a collection of data processing pipelines running in a [dagster](https://dagster.io/) instance
  * These pipelines turn the raw game telemetry into useful stats for the Wrapped report
  * Written in Python
* [Webapp](/apps/webapp/README.md)
  * This is the Web App that users will go to to see their Wrapped report
  * Written in TBD

## Repository Structure & Basic Setup

Here are the relevant directories for each component:
* The ingestor: `apps/ingestor/`
* The analytics: `apps/analytics/`
* The webapp: `apps/webapp/`
* The plugin: `apps/plugin/`

There is also common python code that can be shared between the ingestor and analytics projects in the `common/` directory.

In order to run code that uses the `common` package you'll need to add it to your python path, it's also worth adding the two python projects to the python path also. This can be done by setting the `PYTHONPATH` environment variable to the root of the repository. This can be done in a bash shell with the following command:

```bash
export PYTHONPATH=./common:./apps/ingestor:./apps/analytics
```

For vscode (and many other development environments) you can use a .env file to set environment variables. You can create a file called `.env` in the root of the repository and add the following line to it:

```bash
PYTHONPATH=./common:./apps/ingestor:./apps/analytics
```

The "python path" is a list of directories that python will look in when you try to import a package. You can read more about it [here](https://docs.python.org/3/tutorial/modules.html#the-module-search-path).

## Relevant Tutorials

I have linked a bunch of relevant tutorials for spooling up [here](/tutorials/)
