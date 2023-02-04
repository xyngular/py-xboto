"""
You can import any client boto supports from this module and use it as if that's the current,
thread-safe client.

There are type-hints on the module for common clients we use,
but you can import anything boto supports.

If you import something boto does not support, you'll get an error only when you first
attempt to use the imported client.

```python
# Simply import and use it as-if it's a ready-to-go client.
# (you can use `xyn_aws.clients` for clients)
from xyn_aws.clients import ssm

# You can use it just like the normal boto3 ssm client.
# Every time you use it, it will lazily lookup the current one for the current thread.
ssm_paginator = ssm.get_paginator('get_parameters_by_path')
```

Lazily creating the clients helps support unit-testing with moto,
also reusing the same client lets boto reuse the same connection.

This module allows you to easily share them in a way that supports not directly
tying code together.

If you have an aws client that uses a `-` for it's name, you can use an `_` (underscore)
instead.
All underscores are changed to a `-` when looking up the aws client.
You can also directly use the `xyn_aws.proxy.Boto3Clients.load` method, and use a `-` there.

"""
from typing import Any

from .dependencies import Boto3Clients

# These annotations are only for IDE-type-completion;
# any client boto supports will work when asked for.
# if you ask for an unsupported boto client, error will be raised when you first use it
# (not when you import it).
ssm: Any
secretsmanager: Any
sqs: Any
s3: Any
apigateway: Any

# Underscores are turned into `-` for us when client/resource is looked-up
ecr_public: Any


def __getattr__(name: str):
    if name.startswith("_"):
        raise AttributeError(f"module {__name__} has no attribute {name}")
    return ActiveResourceProxy(Boto3Clients, grabber=lambda clients: getattr(clients, name))
