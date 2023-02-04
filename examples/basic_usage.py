import os
import boto3
from pprint import pprint

from pydantic import BaseModel

from xyn_aws.dynamodb.table import DynamoDBTable
from xyn_aws.models.dynamodb import DynamoDBResultData

DYNAMODB_PORT = os.getenv("DYNAMODB_PORT")


# Create an exiting model
class Person(BaseModel):
    id: int
    first_name: str
    last_name: str


# Create a new table object
dynamodb = boto3.resource("dynamodb", endpoint_url=f"http://localhost:{DYNAMODB_PORT}")

person_table = DynamoDBTable(
    model=Person,
    table_name="offline-Person",
    hash_key="id",
    dynamodb_resource=dynamodb,
)

# Create the table for development (in prod it is done via CloudFormation)
try:
    res = person_table.create_table()
    print("Table created, skipping creation")
except dynamodb.meta.client.exceptions.ResourceInUseException:
    print("Table exists, skipping creation")


# create objects and write them to the database table.
person1 = Person(id=1, first_name="FirstName1", last_name="LastName1")
response = person_table.put_item(obj=person1)
person2 = Person(id=2, first_name="FirstName2", last_name="LastName2")
response = person_table.put_item(obj=person2)
person3 = Person(id=3, first_name="FirstName3", last_name="LastName3")
response = person_table.put_item(obj=person3)

# Delete an item
person_table.delete_item(person2)

# get everything
response = person_table.get_all()


pprint(response)
# Output:
#
# DynamoDBResultData(
#     items=[
#         Person(id=1, first_name='FirstName1', last_name='LastName1'),
#         Person(id=3, first_name='FirstName3', last_name='LastName3')
#     ],
#     count=2,
#     last_item=None
# )

assert isinstance(response, DynamoDBResultData)
assert response.count == 2
assert response.items[0] == person1
assert response.items[1] == person3
