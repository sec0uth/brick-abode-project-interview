"""Test `juniper.cli` module."""

import sys
import os

import pytest
from juniper import cli


def test_get_config_file_takes_sys_argv_first(monkeypatch):
    """Read config file from script arguments event when has environment variable."""
    expected = 'foo.sys.first'

    os.environ[cli.CONFIG_ENV_NAME] = 'foo.env'
    monkeypatch.setattr(sys, 'argv', [None, expected])

    result = cli.deduce_config_file()

    assert result == expected


def test_get_config_file_from_sys_argv(monkeypatch):
    """Read the first script argument as the config file."""
    expected = 'foo.sys'

    monkeypatch.setattr(sys, 'argv', [None, expected])

    result = cli.deduce_config_file()

    assert result == expected


def test_get_config_file_from_env_variable(monkeypatch):
    """Read the config file from environment variable."""
    expected = 'foo.env'

    os.environ[cli.CONFIG_ENV_NAME] = expected

    result = cli.deduce_config_file()

    assert result == expected


def test_fail_to_get_config_file(monkeypatch):
    """Fail to read the config file."""
    if os.getenv(cli.CONFIG_ENV_NAME):
        del os.environ[cli.CONFIG_ENV_NAME]

    monkeypatch.setattr(sys, 'argv', [])

    with pytest.raises(TypeError):
        cli.deduce_config_file()
