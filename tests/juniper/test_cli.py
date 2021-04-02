"""Test `juniper.cli` module."""

import os
import sys
from pathlib import Path

import pytest

from juniper import cli, task


@pytest.fixture
def script_factory(monkeypatch) -> callable:
    """Patch `sys.argv` to mimic script arguments."""
    def factory(*args) -> None:
        monkeypatch.setattr(sys, 'argv', ['fake-script', *args])

    return factory


## deduce_config_file()
#################################


def test_get_config_file_takes_sys_argv_first(script_factory):
    """Read config file from script arguments event when has environment variable."""
    expected = 'foo.sys.first'

    os.environ[cli.CONFIG_ENV_NAME] = 'foo.env'

    # set script argument
    script_factory(expected)

    result = cli.deduce_config_file()

    assert result == expected


def test_get_config_file_from_sys_argv(script_factory):
    """Read the first script argument as the config file."""
    expected = 'foo.sys'

    script_factory(expected)

    result = cli.deduce_config_file()

    assert result == expected


def test_get_config_file_from_env_variable():
    """Read the config file from environment variable."""
    expected = 'foo.env'

    os.environ[cli.CONFIG_ENV_NAME] = expected

    result = cli.deduce_config_file()

    assert result == expected


def test_fail_to_get_config_file(script_factory):
    """Fail to read the config file."""
    if os.getenv(cli.CONFIG_ENV_NAME):
        del os.environ[cli.CONFIG_ENV_NAME]

    # unset script parameters
    script_factory()

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
                                               ctx_manager_factory,
                                               script_factory):
    """Call tasks simulating a script call."""
    # patch script arguments with a template configuration
    script_factory(cfg_template)

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


def test_bind_config_once(monkeypatch, 
                          mock_factory, 
                          cfg_template,
                          ctx_manager_factory,
                          script_factory):
    """Bind `jnpr.junos.utils.config.Config` for each task run."""
    # patch script arguments with a template configuration
    script_factory(cfg_template)

    # fake device
    monkeypatch.setattr(cli, 'make_device', ctx_manager_factory)

    # keep mock to assert how many times was called
    mock_config = mock_factory(side_effect=ctx_manager_factory)

    monkeypatch.setattr(cli,
                        'Config',
                        mock_config)

    # generate 5 tasks
    task_list = [mock_factory() for _ in range(5)]

    # override tasks to run
    monkeypatch.setattr(task, 
                        'load_list', 
                        mock_factory(return_value=task_list))

    cli.main()

    mock_config.assert_called_once()
