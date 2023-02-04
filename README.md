# Xyngular AWS Library

Latest documentation can be reached at [<http://devdocs.xyngular.net/py-xyn-aws/latest/index.html>](<http://devdocs.xyngular.net/py-xyn-aws/latest/index.html>)

AWS utilities to help working aws services and with boto3.


## Import Client

```python

# Use imported `dynamodb` just like dynamodb boto resource
from xyn_aws.resources import dynamodb

# Use imported `ssm` just like ssm boto client
from xyn_aws.clients import ssm

# These are for overriding/injecting settings.
from xyn_aws import Boto3Resources, Boto3Clients, BotoSession

# Can use them like normal:
dynamodb.table(...)
ssm.get_object(...)


# Or you can override settings if you wish:
with Boto3Resources.DynamoDB(region_name='us-west-2'):
    # Use us-west-2 when using dynamodb boto resource:
    dynamodb.table(...)

with Boto3Clients.Ssm(region_name='us-west-2'):
    # Use us-west-2 when using ssm boto client:
    ssm.get_object(...)

with BotoSession(region_name='us-west-3'):
    # Use us-west-3 when using any client/resource
    # we are setting it at the boto-session level;
    # the session is used by all boto client/resources.
    ssm.get_object(...)

    
# Can use them like decorators as well:
@Boto3Clients.Ssm(region_name='us-west-2')
def some_method():
    ssm.get_object(...)

```
