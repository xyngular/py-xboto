from xboto.resource import dynamodb
from xboto.dependencies import BotoResources


def test_endpoint_url_change():
    # We start out with the default endpoint (as long as default AWS_REGION is us-east-1),
    # as the Boto3Settings.endpoint_url has not been set to anything yet.
    assert dynamodb.meta.client.meta.endpoint_url == "https://dynamodb.us-east-1.amazonaws.com"

    with BotoResources.DynamoDB(region_name='us-west-3'):
        assert (
            dynamodb.meta.client.meta.endpoint_url == "https://dynamodb.us-west-3.amazonaws.com"
        )

    # An explicitly provided `endpoint_url` should override default one via Boto3Settings...
    with BotoResources.DynamoDB(endpoint_url='http://localhost:321'):
        assert dynamodb.meta.client.meta.endpoint_url == "http://localhost:321"

    # After we `uninject` the DynamoDB object we just injected, should go back to normal...
    assert dynamodb.meta.client.meta.endpoint_url == "https://dynamodb.us-east-1.amazonaws.com"


def test_endpoint_url_none():
    assert dynamodb.meta.client.meta.endpoint_url == "https://dynamodb.us-east-1.amazonaws.com"
