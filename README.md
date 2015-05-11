A Python SDK for accessing your Trackvia application data.

## Features

1. Simple client to access the Trackvia API
 
## API Access and The User Key

Obtain a user key by enabling the API at:

  https://go.trackvia.com/#/my-info

Note, the API is only available for Enterprise level accounts

## Installation

Install from source
    git clone https://github.com/Trackvia/API-Python-SDK.git
    cd API-Python-SDK
    python setup.py install

## Usage

First you must import the library with
    import trackvia

And then you will need to instantiate a trackvia clien object with
    trackvia = trackvia(url, username, password, userkey);

for usage information, you should be able to read the documentation with
    pydoc trackvia
