import pytest
import moto
from xboto.resource import dynamodb
from xboto.client import ssm
import os

# Ensure we don't have any real keys/id's; just in case.
os.environ['AWS_ACCESS_KEY_ID'] = ''
os.environ['AWS_SECRET_ACCESS_KEY'] = ''
os.environ['AWS_SESSION_TOKEN'] = ''


@pytest.fixture(autouse=True)
def mock_dynamodb():
    with moto.mock_dynamodb():
        yield dynamodb


@pytest.fixture(autouse=True)
def mock_ssm():
    with moto.mock_ssm():
        yield ssm

