## Xyngular AWS Library

Latest documentation can be reached at [<http://devdocs.xyngular.net/py-xyn-aws/latest/index.html>](<http://devdocs.xyngular.net/py-xyn-aws/latest/index.html>)

AWS utilities to help working aws services and with boto3.

## Quick Start

### Import Boto Client/Resource

```python

# Use imported `dynamodb` just like dynamodb boto resource
from xboto.resource import dynamodb

# Use imported `ssm` just like ssm boto client
from xboto.client import ssm

# These are for overriding/injecting settings.
from xboto import BotoResources, BotoClients, BotoSession

# Can use them like normal:
dynamodb.table(...)
ssm.get_object(...)


# Or you can override settings if you wish:
with BotoResources.DynamoDB(region_name='us-west-2'):
    # Use us-west-2 when using dynamodb boto resource:
    dynamodb.table(...)

with BotoClients.Ssm(region_name='us-west-2'):
    # Use us-west-2 when using ssm boto client:
    ssm.get_object(...)

with BotoSession(region_name='us-west-3'):
    # Use us-west-3 when using any client/resource
    # we are setting it at the boto-session level;
    # the session is used by all boto client/resources.
    ssm.get_object(...)

    
# Can use them like decorators as well:
@BotoClients.Ssm(region_name='us-west-2')
def some_method():
    ssm.get_object(...)

```

### Grab Any Client/Resource

```python

# Can easily ask these for any client/resource
from xboto import boto_clients, boto_resources

# These are for overriding/injecting settings.
from xboto import BotoResources, BotoClients, BotoSession

# Can use them like normal:
boto_clients.dynamodb.table(...)
boto_resources.ssm.get_object(...)


# Or you can override settings if you wish:
with BotoResources.DynamoDB(region_name='us-west-2'):
    # Use us-west-2 when using dynamodb boto resource:
    boto_resources.dynamodb.table(...)

with BotoClients.Ssm(region_name='us-west-2'):
    # Use us-west-2 when using ssm boto client:
    boto_clients.ssm.get_object(...)

with BotoSession(region_name='us-west-3'):
    # Use us-west-3 when using any client/resource
    # we are setting it at the boto-session level;
    # the session is used by all boto client/resources.
    boto_clients.ssm.get_object(...)

    
# Can use them like decorators as well:
@BotoClients.Ssm(region_name='us-west-2')
def some_method():
    boto_clients.ssm.get_object(...)

```
