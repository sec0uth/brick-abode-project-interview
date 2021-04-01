"""Test `juniper.task.ssh_passwd` module."""


from juniper.task import ssh_passwd


def test_ask_password_when_needed(mock_factory, getpass_mock):
    """Ask user password when match condition."""
    config = {
        'ssh': {
            'ask_passwd': True,
        }
    }

    task = ssh_passwd.SSHPassword(mock_factory(), config)

    # trigger action
    task.pre_start()

    getpass_mock.assert_called_once()


def test_set_user_password_on_device(mock_factory, getpass_mock):
    """Set password on device."""
    expected_passwd = 'h4ckme'

    # force ask the password
    config = {
        'ssh': {
            'ask_passwd': True,
        },
    }

    getpass_mock.return_value = expected_passwd

    # keep mock to make assertions about password
    mock_dev = mock_factory()

    task = ssh_passwd.SSHPassword(mock_dev, config)

    # trigger action
    task.pre_start()

    assert mock_dev._auth_password == expected_passwd


def test_not_ask_password_when_not_explicitly_asked(mock_factory, getpass_mock):
    """Do not ask for password when `ask_passwd` is not `True`."""
    # force NOT to ask the password
    config = {
        'ssh': {
            'ask_passwd': 'whatever',
        },
    }

    task = ssh_passwd.SSHPassword(mock_factory(), config)

    # trigger action
    task.pre_start()

    getpass_mock.assert_not_called()


def test_not_ask_password_when_asked_but_password_is_set(mock_factory, getpass_mock):
    """Do not ask for password when `ask_passwd` is `True` but `passwd` is not null."""
    # force ask the password
    config = {
        'ssh': {
            'passwd': '',
            'ask_passwd': True,
        },
    }

    task = ssh_passwd.SSHPassword(mock_factory(), config)

    # trigger action
    task.pre_start()

    getpass_mock.assert_not_called()