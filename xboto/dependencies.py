"""
A few classes/resources that let you use a lazily created boto resource/client,
in a thread-safe manner:

Normally, you would just get it via an attribute name, in this version you

>>> aws_clients.ssm.get_paginator()

Or you can import it like so:

>>> from xyn_aws.clients import ssm
>>> ssm.get_paginator()

Same with resources:

>>> aws_resources.dynamodb.Table("some-table")

Or

>>> from xyn_aws.clients import dynamodb
>>> dynamodb.Table("some-table")
"""
from typing import Any, Optional, Dict, Type, Callable

import boto3
import botocore
from botocore.session import Session
from xsentinels import Singleton
from xinject import Dependency, XContext


class BotoSession(Dependency):
    """
    You can use this as an easy way to get a shared boto-session for the current thread.

    Right now only used with `_Loader` subclasses such as `Boto3Clients` and `Boto3Resources`.

    Boto Sessions are NOT thread-safe.
    When user is not using a session to create a client/resource,
    boto3 uses an internal/default session instead which is not thread-safe.

    - Or the docs for boto about this:
        - https://boto3.amazonaws.com/v1/documentation/api/latest/guide/session.html
    - For various examples see issue where people talk about it:
        - https://github.com/boto/botocore/issues/1246
    """

    @property
    def session(self) -> boto3.Session:
        if session := self._session:
            return session
        session = boto3.Session(**self._session_kwargs)
        self._session = session
        return session

    def __init__(
            self, *,
            reset_session_when_activated=False,
            aws_access_key_id: Optional[str] = None,
            aws_secret_access_key: Optional[str] = None,
            aws_session_token: Optional[str] = None,
            region_name: Optional[str] = None,
            botocore_session: Optional[Session] = None,
            profile_name: Optional[str] = None,
            **session_kwargs
    ):
        """

        Args:
            reset_session_when_activated: If True: when self is activated
                (ie: made the current resource/dependency)
                will automatically call `BotoSession.reset_session()`, and therefore next time
                `BotoSession.session` is asked for will lazily allocate new boto Session.
                This is useful for unit-tests, where you really do want to create a new
                session/connection each time the unit-test is called if you use
                `BotoSession` as a decorator to a unit-testing method.

                If False (default): will keep any session that has been previously/lazily created.
                This keeps the connections around for you; hence why it's the default option.

            aws_access_key_id (str):  access key ID
            aws_secret_access_key (str): AWS secret access key
            aws_session_token (str): AWS temporary session token
            region_name (str): Default region when creating new connections
            botocore_session (botocore.session.Session): Use this Botocore session instead of
                creating a new default one.
            profile_name (str): The name of a profile to use. If not given, then the default
                profile is used.
            **session_kwargs: Pass additional args for boto Session here
                (for additional args that boto3 might add in the future).
        """
        # Easily grab all boto args passed into us...
        args = {k: v for k, v in locals().items() if v is not None}
        args.pop('self', None)
        args.pop('reset_session_when_activated', None)
        args.pop('session_kwargs', None)

        # Remember args...
        self.reset_session_when_activated = reset_session_when_activated
        self._session_kwargs = {**args, **session_kwargs}
        self._boto_obj_store = {}

    def context_resource_for_copy(
            self, *, current_context: XContext, copied_context: XContext
    ) -> 'BotoSession':
        if self.reset_session_when_activated:
            self.reset_session()
        return self

    @property
    def session_kwargs(self) -> Dict[str, Any]:
        return self._session_kwargs.copy()

    @session_kwargs.setter
    def session_kwargs(self, value: Dict[str, Any]):
        self._session_kwargs = {**value}
        self.reset_session()

    def reset_session(self):
        # We will lazily create session and their associated boto-objs in the future as needed.
        self._session = None
        self._boto_obj_store = {}

    _session: Optional[boto3.Session] = None
    _session_kwargs: dict
    _boto_obj_store: dict

    def _boto_obj_for_dependency(
            self,
            dependency: '_BaseBotoClientOrResource',
            constructor: Callable,
            force_create: bool = False
    ):
        if not force_create and (boto_obj := self._boto_obj_store.get(dependency)):
            return boto_obj

        boto_obj = constructor()
        self._boto_obj_store[dependency] = boto_obj
        return boto_obj

    def _reset_boto_obj_for_dependency(self, dependency: '_BaseBotoClientOrResource'):
        self._boto_obj_store.pop(dependency, None)


boto_session = BotoSession.resource_proxy()
""" You can use this as the current 'boto' session object.
    `_Loader` subclasses use this right now (see below).
"""


class _BaseBotoClientOrResource(Dependency):
    # Instead of inheriting from `ThreadUnsafeResource`, we set flag directly ourselves.
    # This allows us to be compatible with both v2 and v3 of xyn_resource.
    resource_thread_safe = False

    # Class Vars
    _boto_name: str = ''
    _boto_kind: str = ''

    # Instance Vars

    # These are used to keep track of how we configure(d) the boto client/resource.
    _boto_kwargs: Dict[str, Any]

    def __init__(
            self, region_name=None,
            api_version=None,
            use_ssl=None,
            verify=None,
            endpoint_url=None,
            aws_access_key_id=None,
            aws_secret_access_key=None,
            aws_session_token=None,
            config=None,
            **boto_kwargs
    ):
        """
        You can specify any of the boto client/resource args, the known ones have been
        specififed and documented out.
        
        If there are ones in the future that are new or we don't know about, you can
        still specify them, they will be passed to us in `boto_kwargs`, which will be
        used as addtional kwargs when creating new boto client/resource.
        
        Args:
            region_name: The name of the region associated with the client. A client is associated
                with a single region.
            api_version: The API version to use. By default, botocore will use the latest API
                version when creating a client.You only need to specify this parameter if you want
                to use a previous API version of the client.
            use_ssl: Whether or not to use SSL. By default, SSL is used. Note that not all
                services support non-ssl connections.
            verify: Whether or not to verify SSL certificates. By default SSL certificates are
                verified. You can provide the following values:

                - False - do not validate SSL certificates. SSL will still be used
                    (unless use_ssl is False), but SSL certificates will not be verified.
                - path/to/cert/bundle.pem - A filename of the CA cert bundle to uses.
                    You can specify this argument if you want to use a different CA cert bundle
                    than the one used by botocore.
            endpoint_url: The complete URL to use for the constructed client.
                Normally, botocore will automatically construct the appropriate URL to use when
                communicating with a service. You can specify a complete URL
                (including the "http/https" scheme) to override this behavior.
                If this value is provided, then use_ssl is ignored.
            aws_access_key_id: The access key to use when creating the client.
                This is entirely optional, and if not provided, the credentials configured for the
                session will automatically be used. You only need to provide this argument if you
                want to override the credentials used for this specific client.
            aws_secret_access_key: The secret key to use when creating the client.
                Same semantics as aws_access_key_id above.
            aws_session_token: The session token to use when creating the client.
                Same semantics as aws_access_key_id above.
            config: Advanced client configuration options.
                If region_name is specified in the client config, its value will take precedence
                over environment variables and configuration values, but not over a region_name
                value passed explicitly to the method. If user_agent_extra is specified in the
                client config, it overrides the default user_agent_extra provided by the resource
                API. See
                [botocore config documentation](https://botocore.amazonaws.com/v1/documentation/api/latest/reference/config.html)
                for more details.
            **boto_kwargs:
        """  # noqa -- url can't be broken up.
        # Easily grab all boto args passed into us...
        args = {k: v for k, v in locals().items() if v is not None}
        args.pop('self', None)
        args.pop('boto_kwargs', None)

        self._boto_kwargs = {**args, **boto_kwargs}

    def __init_subclass__(cls, boto_name: str = '', boto_kind: str = '', **kwargs):
        super().__init_subclass__(**kwargs)
        cls._boto_name = boto_name
        cls._boto_kind = boto_kind

    def reset(self):
        """ Resets the client; it will be re-created lazily next time it's asked for.
        """
        # noinspection PyProtectedMember
        BotoSession.grab()._reset_boto_obj_for_dependency(self)

    def get(self):
        # If user specified their own 'endpoint_url', we are not using the default.
        # Otherwise, check to make sure settings value is still same as what we used;
        # we want a new object if the default endpoint_url has changed...
        #
        # For now, we just throw-away any old object if default has changed and user did not
        # specify their own endpoint_url value. If it changes frequently for some reason we
        # could optimize by store a client per-endpoint_url value, so we can reuse old
        # client when old values are restored.

        force_create = 'endpoint_url' not in self._boto_kwargs

        def constructor():
            # `kind` is either 'client' or 'resource', we get the correct creation method...
            boto_creation_method = getattr(boto_session.session, self._boto_kind)

            # We then call creation method with the resource/client name and any other kwargs;
            # For the kwargs, we start with any defaults and then add in user specified ones...
            return boto_creation_method(
                self._boto_name, **self._boto_kwargs
            )

        # noinspection PyProtectedMember
        return BotoSession.grab()._boto_obj_for_dependency(
            self, constructor, force_create=force_create
        )

    @classmethod
    def _get_dependency_cls(cls, boto_name: str) -> 'Type[_BaseBotoClientOrResource]':
        boto_kind = cls._boto_kind

        # Normalize name...
        # Client/Resources names never use `_`, they use a `-` instead.
        # Replace any `_` with a `-`
        # (allows one to still get it via attributes, vs having to pass a str into a/the method)
        boto_name = boto_name.replace("_", "-")
        boto_name = boto_name.lower()

        if dep_cls := _dependency_classes[boto_kind].get(boto_name):
            return dep_cls

        # We are creating a new type/class lazily based on the required boto resource/client...
        cls_name = f'{boto_name.capitalize()}{boto_kind.capitalize()}'
        dep_cls: Any = type(cls_name, (cls,), {}, boto_name=boto_name, boto_kind=boto_kind)

        # Store the type for future use.
        _dependency_classes[boto_kind][boto_name] = dep_cls
        return dep_cls

    @classmethod
    def get_dependency_cls(cls, boto_name: str) -> 'Type[_BaseBotoClientOrResource]':
        raise NotImplementedError("Need to implement `get_dependency_cls` class method")

    @property
    def boto_kwargs(self) -> Dict[str, Any]:
        """
        Returns a copy of the boto_kwargs assigned either while creating object in init
        `_BaseBotoClientOrResource.__init__ or changed via `boto_kwargs` setter property
        after it was created.

        Any settings defined in dict will be passed to boto-client/resource when it's lazily
        created.
        """
        return self._boto_kwargs.copy()

    @boto_kwargs.setter
    def boto_kwargs(self, value: Dict[str, Any]):
        """
        Makes a copy of value and will use them as the boto_kwargs.

        Any settings defined in dict will be passed to boto-client/resource when it's lazily
        created.

        After property is set, will call `_BaseBotoClientOrResource.reset` so that the next
        time that a boto-client/resource is asked of me I'll lazily create a new client/resource
        with the setting provided to this property-setter.
        """
        self._boto_kwargs = {**value}
        self.reset()


class BotoClient(_BaseBotoClientOrResource, boto_kind='client'):
    @property
    def boto_client(self):
        return self.get()

    @classmethod
    def get_dependency_cls(cls, boto_name: str) -> 'Type[BotoClient]':
        return cls._get_dependency_cls(boto_name)


class BotoResource(_BaseBotoClientOrResource, boto_kind='resource'):
    @property
    def boto_resource(self):
        return self.get()

    @classmethod
    def get_dependency_cls(cls, boto_name: str) -> 'Type[BotoResource]':
        return cls._get_dependency_cls(boto_name)


_dependency_classes: Dict[str, Dict[str, Type[BotoClient]]] = {
    'resource': {},
    'client': {}
}


class _LoaderMetaclass(type):
    _boto_dependency_class: Type[_BaseBotoClientOrResource]

    def __getattr__(self, key: str):
        if not key[0].isupper():
            raise AttributeError(
                f"BotoClient/BotoResource classes start with an upper-case char, "
                f"was instead given ({key})."
            )
        try:
            return self._boto_dependency_class.get_dependency_cls(key)
        except Exception as e:
            raise AttributeError(
                f"BotoClient/BotoResource class does not exist for key ({key}) "
                f"start with an upper-case char, was instead given ({key})."
            )


class _Loader(Singleton, metaclass=_LoaderMetaclass):
    def __init_subclass__(
            cls, boto_dependency_class: Optional[Type[_BaseBotoClientOrResource]] = None, **kwargs
    ):
        assert boto_dependency_class, (
            f"Subclass {cls} need to pass in `boto_dependency_class` class arg."
        )
        cls._boto_dependency_class = boto_dependency_class

    def load(self, module):
        """
        This is a way you can use a dynamic string to grab a boto3 client/resource by name.

        Normally, you would want to use one of these ways of doing it instead:

        >>> from xyn_aws import aws_clients
        >>> aws_clients.ssm

        Or you can import it like so:

        >>> from xyn_aws.clients import ssm

        And then you can use this ssm client just like the real one:

        >>> ssm.get_paginator(...)

        There are also equivelent things for resources (like the client examples above)
        at `xyn_aws.resources` and `xyn_aws.aws_resources`.

        If you want to use a normal string to look up the client or resource,
        that's when you can use this load method.

        You can look up a boto3 client/resource via this method by passing in its name.
        You'll want to use a subclass of `_Loader` such as `Boto3Clients` or `Boto3Resources`.

        See thoese classes for more details, here are some quick examples:

        >>> Boto3Resources.grab().load('dynamodb')

        or

        >>> aws_resources.load('dynamodb')

        or

        >>> Boto3Clients.grab().load('ssm')

        or

        >>> aws_clients.load('ssm')
        """

        # We cache the clients/resources directly on 'self' (object),
        # using `module` as the attr-name (see `_Loader.__getattr__`)
        return getattr(self, module)

    def _lookup(self, module):
        """Implemented in subclasses to look up the module from boto3 properly."""
        raise NotImplementedError(f"Need to implement `_lookup` in subclass ({self}).")

    def __getattribute__(self, item):
        """
        Grabs a client/resource and stores it on self, returns it.

        Args:
            item: item-name to get

        Returns:

        """
        try:
            return super().__getattribute__(item)
        except AttributeError:
            client = self._lookup(item)
            return client


class Boto3Clients(_Loader, boto_dependency_class=BotoClient):
    """
    When you get an attribute off of me, I'll attempt to ask the boto3 library to allocate
    a client of the same type, and then store itself, so I return the same client again
    in the future.

    Right now, we will lazily allocate a boto3 client per-thread, and we will use the
    per-thread shared boto3 session resource to do it (ie: `_BotoSession.session`).

    You can also easily import and use the `aws_clients` proxy object
    (defined at top module-level).

    You can use `aws_clients` exactly the same as using `Boto3Clients.grab()`,
    making it more convenient to use since you can directly import `aws_clients`.

    >>> from xyn_aws import aws_clients
    >>> # Showing here how you could use it:
    >>> aws_clients.ssm.get_paginator(...)

    If you have an aws client that uses a `-` for it's name, you can use an `_` (underscore)
    instead.
    All underscores are changed to a `-` when looking up the aws client.
    You can also directly use the `xyn_aws.proxy.Boto3Clients.load` method, and use a `-` there.
    """

    def _lookup(self, module):
        return BotoClient.get_dependency_cls(module).grab().boto_client

    # These annotations are only for IDE-type-completion;
    # any client boto supports will work regardless (even if not listed below).
    #
    # These are the xyn-resource `Resource` types/classes; ie: BotoClient subclasses
    # (start with upper-case letter)
    DynamoDB: Type[BotoClient]
    Ssm: Type[BotoClient]
    SecretsManager: Type[BotoClient]
    S3: Type[BotoClient]
    ApiGateway: Type[BotoClient]

    # These annotations are only for IDE-type-completion;
    # any client boto supports will work regardless (even if not listed below).
    #
    # These are the boto client objects (start with lower-case letter)
    ssm: Any
    secretsmanager: Any
    sqs: Any
    s3: Any
    apigateway: Any


class Boto3Resources(_Loader, boto_dependency_class=BotoResource):
    """
    When you get an attribute off of me, I'll attempt to ask the boto3 library to allocate
    a resource of the same type, and then store itself, so I return the same resource again
    in the future.

    Right now, we will lazily allocate a boto3 resource per-thread, and we will use the
    per-thread shared boto3 session resource to do it (ie: `_BotoSession.session`).

    You can also easily import and use the `aws_resources` proxy object
    (defined at top module-level).

    You can use `aws_resources` exactly the same as using `Boto3Resources.grab()`,
    making it more convenient to use since you can directly import `aws_resources`.

    >>> from xyn_aws import aws_resources
    >>> # Showing here how you could use it to get a Table resource:
    >>> table = aws_resources.dynamodb.Table("some-table")

    If you have an aws resource that uses a `-` for it's name, you can use an `_` (underscore)
    instead.
    All underscores are changed to a `-` when looking up the aws resource.
    You can also directly use the `xyn_aws.proxy.Boto3Resources.load` method, and use a `-` there.
    """

    def _lookup(self, module, **kwargs):
        return BotoResource.get_dependency_cls(module).grab().boto_resource

    # These annotations are only for IDE-type-completion;
    # any client boto supports will work regardless (even if not listed below).
    #
    # These are the xyn-resource `Resource` types/classes; ie: BotoResource subclasses
    # (start with upper-case letter):
    DynamoDB: Type[BotoResource]
    CloudFormation: Type[BotoResource]
    CloudWatch: Type[BotoResource]
    Ec2: Type[BotoResource]
    Glacier: Type[BotoResource]
    Iam: Type[BotoResource]
    OpsWorks: Type[BotoResource]
    S3: Type[BotoResource]
    Ns: Type[BotoResource]
    Sqs: Type[BotoResource]

    # These annotations are only for IDE-type-completion;
    # any client boto supports will work regardless (even if not listed below).
    #
    # These are the boto resource objects (start with lower-case letter):
    dynamodb: Any
    cloudformation: Any
    cloudwatch: Any
    ec2: Any
    glacier: Any
    iam: Any
    opsworks: Any
    s3: Any
    ns: Any
    sqs: Any


aws_clients = Boto3Clients()
""" You can import this and then ask it for clients via attributes.

    Example:

    >>> from xyn_aws import aws_clients
    >>>
    >>> # Get the ssm client (ask for it each time), then get it's paginator.
    >>> aws_clients.ssm.get_paginator(...)

    You can also directly import a client like so:

    >>> from xyn_aws.clients import ssm
    >>>
    >>> # You can just use it directly anytime you need too:
    >>> ssm.get_paginator()
"""

aws_resources = Boto3Resources()
""" You can import this and then ask it for clients via attributes.

    Example:

    >>> from xyn_aws import aws_resources FINISH HERE!!!!! ****
    >>>
    >>> # Get the ssm client (ask for it each time), then get it's paginator.
    >>> aws_clients.ssm.get_paginator(...)

    You can also directly import a client like so:

    >>> from xyn_aws.clients import ssm
    >>>
    >>> # You can just use it directly anytime you need too:
    >>> ssm.get_paginator()
"""
