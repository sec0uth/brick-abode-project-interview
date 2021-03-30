"""Configure global fixtures."""


from unittest.mock import Mock

from jnpr.junos import Device


def device_factory() -> Device:
    """Return a mocked device object."""
    return Mock