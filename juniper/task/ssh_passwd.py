"""Set ssh password on Juno device in runtime."""


import getpass

from . import abc


class SSHPassword(abc.AbstractTask):
    """Ask for password on `pre_start()` call then send to device."""

    def pre_start(self):
        """Ask password when needed."""
        ssh_config = self.config['ssh']

        needs_passwd = ssh_config.get('passwd') is None and \
                        ssh_config.get('ask_passwd') is True

        if needs_passwd:
            # ask user password
            ssh_passwd = getpass.getpass(prompt='SSH password:')

            # set auth password
            self.dev._auth_password = ssh_passwd

    def run(self):
        """Task do anything at all."""
        pass