# Webapp

This will contain the Frontend (FE) and Backend (BE) for the final website that users will go to to see their Runelite Wrapped slide show!

## Overview

This part of the project is still a massive WIP, but here is a rough outline

* Backend will query the mongo database for the pipeline outputs for a given user
* Frontend will create a pretty display of the Wrapped report
* We will need authentication, so people's reports are not public by default
  * Multiple osrs users per account 😱, maybe a key that needs to be linked with the plugin?
* We will want to implement sharable links, so people can share their reports

## FE

Frontend is located at [fe](./fe)

It is written using Vue.js 3 and TypeScript

## Setup

You will need to install nodejs and npm

To install dependencies, `cd` into the fe folder and run:
```sh
npm install
```

To run a development server run:
```sh
npm run serve
```


## BE

TODO

Will be located in [be](./be)

Will be written in python using FastAPI
