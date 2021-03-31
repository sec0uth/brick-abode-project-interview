"""Test `juniper.cli` module."""

import os
import sys
from pathlib import Path

import pytest

from juniper import cli


## deduce_config_file()
#################################


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


## make_device()
#################################


def test_use_device_with_default_settings(tmp_path):
    """Make device with default settings when missing ssh config."""
    expected_hostname = 'foo.baz.me'

    # create empty file
    dummy_ssh_config = tmp_path / Path('ssh_config')
    dummy_ssh_config.write_text('')

    the_config = {
        'ssh': {
            'config': dummy_ssh_config.name,
            'host': expected_hostname,
        },
    }

    device = cli.make_device(the_config)

    assert device._ssh_config == dummy_ssh_config.name
    assert device.port == 22
    assert device.hostname == expected_hostname