A Python SDK for accessing your Trackvia application data.

## Features

1. Simple client to access the Trackvia API
 
## API Access and The User Key

Obtain a user key by enabling the API at:

  https://go.trackvia.com/#/my-info

Note, the API is only available for Enterprise level accounts

## Usage

First instantiate a TrackViaClient object

TrackViaClient client = TrackviaClient.create(path, scheme, hostName, port, email, password, userKey);

The client interface is more fully explained in the Java Docs and our Tic-tac-toe tutorial: https://developer.trackvia.com/tutorials/tic-tac-toe
