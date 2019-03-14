# python-userful

Unofficial Python Client For Userful API. Note that this client is not feature complete, calls will be
added as they are required.

# Usage

All client methods return a `requests.Response` object. None of them do status checking, it
is up to the user of the client to decide whether to check the return status code.

## Initialization

The client can be configured either using environment variables or when instantiating the client.

If authentication fails due to a misconfiguration, a `requests.exceptions.HTTPError` will be raised.

### Using Environment Variables

The following environment variables can be used to configure the client:

* USERFUL_USER - username for authentication (required)
* USERFUL_PASS - password for authentication (required)
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
