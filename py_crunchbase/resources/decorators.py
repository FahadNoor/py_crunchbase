from typing import Union, Type

from .base import Resource
from .registry import ResourceRegistry


def extend_cb_resource(name_or_resource: Union[str, Type[Resource]]):
    """
    This decorator can be used to extend any existing Resource class
    A use case can be that you need to add a property in Organization class that returns True if the organization
    is acquired

    @extend_cb_resource
    class Organization(CBR.Organization):

        @property
        def is_acquired(self) -> bool:
            return self.status == 'was_acquired'

    Now CBR.Organization will return this new class
    org = CBR.Organization(data)
    if org.is_acquired:
        print('not interested')

    extend_cb_resource accepts an optional name argument
    @extend_cb_resource('Organization')
    class MyCustomResource(CBR.Organization):
        pass

    CBR.Organization will return MyCustomResource
    """
    if not isinstance(name_or_resource, str):
        ResourceRegistry.add_resource(name_or_resource)
        return name_or_resource

    def decorator(resource_cls: Type[Resource]):
        ResourceRegistry.add_resource(resource_cls, name_or_resource)
        return resource_cls

    return decorator
