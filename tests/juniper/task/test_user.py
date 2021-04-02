"""Test `juniper.task.user` module."""


import pytest

from juniper.task import user


@pytest.fixture(scope='function')
def task(mock_factory):
    """Return an instance of `juniper.task.user.UserManagement`."""
    config = {
        'changes': {
            'user': {
                'name': 'testuser',
                'passwd': 'h4ckme',
                'class': 'baz',
            }
        }
    }

    return user.UserMgmtTask(mock_factory(), config)


def test_ask_user_password_when_missing(task, getpass_mock):
    """Ask for user password when `passwd` is missing."""
    # unset password
    task.changes['user'].update(passwd=None)

    task.pre_start()

    getpass_mock.assert_called_once()


def test_update_user_provided_password(task, getpass_mock):
    """Update internal config with user password."""
    expected_passwd = '1234'

    # force to ask the password
    task.changes['user'].update(passwd=None)

    getpass_mock.return_value = expected_passwd 

    task.pre_start()

    assert task.changes['user']['passwd'] == expected_passwd


def test_load_command_with_user_name_and_class(task, mock_factory):
    """Call user command with user's name and class."""
    config = {
        'name': 'fooName',
        'class': 'bazClass',
    }

    task.changes['user'].update(**config)

    # patch dev configuration
    task.dev.cu = mock_factory()

    task.run()

    task.dev.cu.load.assert_called_once()

    command = task.dev.cu.load.call_args[0][0]

    assert config['name'] in command
    assert config['class'] in command


def test_commits_configuration_finally(task, mock_factory):
    """Commit configuration at the end."""
    # patch dev configuration
    task.dev.cu = mock_factory()

    # trigger
    task.run()

    task.dev.cu.commit.assert_called_once()
