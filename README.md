A Python SDK for accessing your Trackvia application data.

## Features

1. Simple client to access the Trackvia API

## API Access and The User Key

Obtain a user key by enabling the API at: https://go.trackvia.com/#/my-info

Note, the API is only available for Enterprise level accounts

## Installation

### Install via pip
```bash
pip install trackvia
```

### Install from source
You can install this module from source by checking it out and running setup.py. Keep in mind that this module requires urllib3, httplib, and requests.
```bash
    git clone https://github.com/Trackvia/API-Python-SDK.git
    cd API-Python-SDK
    python setup.py install
```

## Usage

First you must import the library and instantiate the trackvia client object
```python
import trackvia
trackvia = trackvia.trackvia(url, username, password, userkey)

#create 2 new records in view ID 3
record1 = {'name': 'John White', 'age': 35}
record2 = {'name': 'Charlotte Green', 'age': 29}
records = [record1, record2]

trackvia.create_record(3, records)
```

for more information, you can use pydoc on the command line to read the documentation `pydoc trackvia`
