import os

import boto3
from pydantic import BaseModel
from xyn_aws.dynamodb import DynamoDBTableMixin

DYNAMODB_PORT = os.getenv("DYNAMODB_PORT")


dynamodb = boto3.resource("dynamodb", endpoint_url=f"http://localhost:{DYNAMODB_PORT}")


class Person(DynamoDBTableMixin):
    id: int
    first_name: str
    last_name: str

    class DynamoDBConfig:
        table_name = "offline-Person"
        hash_key = "id"
        dynamodb_resource = dynamodb


# create person object
person = Person(id=1, first_name="FirstName1", last_name="LastName1")

# save to table with the new `dynamodb` attribute
person.dynamodb.save()

# Use standard calls are still available with `.table` attribute
original_person = person.dynamodb.table.get_item(hash_key_value=person.id)

assert person == original_person

# change object
person.first_name = "ChangeFirstName"
save_response = person.dynamodb.save()

# compare to original
print(person)
# id=1 first_name='ChangeFirstName' last_name='LastName1'

print(save_response)
# id=1 first_name='FirstName1' last_name='LastName1'

# Response from save is the original object
assert save_response == original_person

# delete
deleted_person = person.dynamodb.delete()

# response from delete is the object before deletion
assert deleted_person == person

# item is no longer in table
query_for_deleted = person.dynamodb.table.get_item(hash_key_value=person.id)
assert query_for_deleted is None
