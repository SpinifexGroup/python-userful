# python-userful

Unofficial Python Client For [the Userful REST API](http://dev.userful.com/rest/#).

Note that this client is not feature complete, calls will be added as they are required.

# Usage

All client methods return a `requests.Response` object. None of them do status checking, it
is up to the user of the client to decide whether to check the return status code.

## Initialization

The client can be configured either using environment variables or when instantiating the client.

If authentication fails due to a misconfiguration, a `requests.exceptions.HTTPError` will be raised.

### Using Environment Variables

The following environment variables can be used to configure the client:

* USERFUL_USER - username for authentication (required)
* USERFUL_PASS - password for authentication (required). Keep in mind that storing secrets in environment
  variables can be hazardous. As such, you might want to provide your password during instiation instead.
* USERFUL_HOST - hostname or IP address of userful API (required)
* USERFUL_PORT - port of userful API (optional, defaults to `9000`)

After exporting these variables, the client can be instantiated as follows:

```
from userful.client import UserfulClient

client = UserfulClient()
```

### Passing during initialization
```
from userful.client import UserfulClient

client = UserfulClient(user="myuser", password="s00persecret", host="myuserfulhost.com")
```

# Recipes

## Switching the source on a zone
```
# Change the source of the zone. This DOES NOT actually change what is on the screen.
# However, this source now becomes the default for the zone.
client.switch_source_by_zone('Zone-0', 'Userful Desktop')

# Actually make the zone start playing the new source
client.play_by_zone('Zone-0')
```

## Updating an existing source
```
# The PUT call to update a source is not idempotent, so we need to start by
# grabbing the existing source object

payload = client.get_sources(name='my_source')

# Get the ID of the source
source_id = payload['sourceId']

# Change the name of the source in the payload
payload['sourceName'] = 'my_new_source_name'

# Send the new data to the API
res = client.update_source(source_id, payload)
```
