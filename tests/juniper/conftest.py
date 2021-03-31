"""Configure global fixtures."""


import os
import contextlib
from unittest.mock import Mock

import pytest
from jnpr.junos import Device


@pytest.fixture
def mock_factory() -> Mock:
    """Return a factory to mock objects."""
    return Mock


@pytest.fixture
def ctx_manager_factory() -> Mock:
    """
    Return a factory to `with` statement context managers.

    Example:
    ```
    def test_foo_bar(ctx_manager_factory):
        open_mock = ctx_manager_factory

        with open_mock('baz.py', mode='r') as reader:
            pass
    ```
    """

    @contextlib.contextmanager
    def factory(*_, **__):
        yield

    return factory


@pytest.fixture
def cfg_template() -> str:
    """Return the path a configuration template."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_dir,
                        'assets',
                        'cfg_template.yaml')
