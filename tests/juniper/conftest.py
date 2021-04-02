"""Configure global fixtures."""


import contextlib
import datetime
import getpass
import os
from unittest.mock import Mock

import pytest
from jnpr.junos import Device


@pytest.fixture
def mock_factory() -> Mock:
    """Return a factory to mock objects."""
    return Mock


@pytest.fixture
def ctx_manager_factory(mock_factory) -> contextlib.AbstractContextManager:
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
        if 'return_value' in __:
            yield __['return_value']
        else:
            yield mock_factory()

    return factory


@pytest.fixture
def cfg_template() -> str:
    """Return the path a configuration template."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_dir,
                        'assets',
                        'cfg_template.yaml')


@pytest.fixture
def getpass_mock(monkeypatch, mock_factory) -> Mock:
    """Patch `getpass.getpass` module."""
    getpass_mock = mock_factory()

    monkeypatch.setattr(getpass, 
                        'getpass',
                        getpass_mock)

    return getpass_mock


@pytest.fixture
def now_mock(monkeypatch, mock_factory):
    """Patch `datetime.datetime.now()` classmethod."""    
    mock_datetime = mock_factory()

    # patch datetime to return test date
    monkeypatch.setattr(datetime, 'datetime', mock_datetime)

    return mock_datetime.now