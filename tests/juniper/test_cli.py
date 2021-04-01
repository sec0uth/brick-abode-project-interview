"""Test `juniper.cli` module."""

import os
import sys
from pathlib import Path

import pytest

from juniper import cli, task


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


## main()
#################################


def test_run_registered_tasks_methods_in_order(monkeypatch, 
                                               mock_factory, 
                                               cfg_template,
                                               ctx_manager_factory):
    """Call tasks simulating a script call."""
    # patch script arguments with a template configuration
    monkeypatch.setattr(sys, 'argv', [None, cfg_template])

    # fake device
    monkeypatch.setattr(cli, 'make_device', ctx_manager_factory)

    # keep object to make assertions
    mock_task = mock_factory()
    
    # ensure `pre_start()` is called before `run()`
    mock_task.pre_start.side_effect = lambda *_,**__: \
                                        mock_task.run.assert_not_called()

    task_list = [mock_factory(return_value=mock_task)]

    # override tasks to run
    monkeypatch.setattr(task, 
                        'load_list', 
                        mock_factory(return_value=task_list))
    
    cli.main()

    mock_task.pre_start.assert_called_once()
    mock_task.run.assert_called_once()