"""Configure global fixtures."""


import os
from unittest.mock import Mock

import pytest
from jnpr.junos import Device


def device_factory() -> Device:
    """Return a mocked device object."""
    return Mock


@pytest.fixture
def cfg_template():
    """Return the path a configuration template."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_dir,
                        'assets',
                        'cfg_template.yaml')