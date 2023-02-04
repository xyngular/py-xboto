import pytest
import moto
from xyn_aws.resources import dynamodb
from xyn_aws.clients import ssm


@pytest.fixture(autouse=True)
def mock_dynamodb():
    with moto.mock_dynamodb():
        yield dynamodb


@pytest.fixture(autouse=True)
def mock_ssm():
    with moto.mock_ssm():
        yield ssm

