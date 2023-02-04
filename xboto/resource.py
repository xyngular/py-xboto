"""
You can import any resource boto supports from this module and use it as if that's the current,
thread-safe resource.

There are type-hints on the module for common resources we use,
but you can import anything boto supports.

If you import something boto does not support, you'll get an error only when you first
attempt to use the imported resource/client.

```python
# Simply import and use it as-if it's a ready-to-go resource.
# (you can use `xboto.client` for clients)
from xboto.resource import dynamodb

# You can use it just like the normal boto3 dynamodb resource.
# Every time you use it, it will lazily lookup the current one for the current thread.
table_resource = dynamodb.Table(name)
```

If you have an aws resource that uses a `-` for it's name, you can use an `_` (underscore)
instead.
All underscores are changed to a `-` when looking up the aws resource.
You can also directly use the `xboto.dependencies.BotoResources.load` method, and use a `-` there.

"""
from typing import Any

from .dependencies import boto_resources

# These annotations are only for IDE-type-completion;
# any resource boto supports will work when asked for.
# If you ask for an unsupported boto resource, error will be raised when you first use it
# (not when you import it).

cloudformation: Any
cloudwatch: Any
dynamodb: Any
ec2: Any
glacier: Any
iam: Any
opsworks: Any
s3: Any
sns: Any
sq: Any


def __getattr__(name):
    if name.startswith("_"):
        raise AttributeError(f"module {__name__} has no attribute {name}")

    # Reserve upper-case for future potential feature (ie: grab dependency class).
    if name[0].isupper():
        raise AttributeError(
            f"module {__name__} has no attribute {name} (use lower-case attr; ie: {name.lower()})."
        )
    from .dependencies import BotoResources
    return BotoResources.proxy_attribute(name)
