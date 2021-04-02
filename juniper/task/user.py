"""Manage user accounts."""

import crypt
import getpass

from . import abc


def secure_hash(password: str) -> str:
    """
    Calculate password secure hash of `password`.
    
    Use sha256 based hash function to keep compatibility with
    other operating systems given that `crypt` module relays on
    OS's routines.
    """
    return crypt.crypt(password, crypt.METHOD_SHA256)


class UserMgmtTask(abc.AbstractTask):
    """Upsert user on system with provided properties."""

    # Juno command to add/edit user
    command_mask = '''set system login user "{name}" class {class} ''' \
                    '''authentication encrypted-password "{encrypted_passwd}"'''

    def pre_start(self):
        """Ask for user password when `passwd` config is missing."""
        # default login class
        self.changes['user'].setdefault('class', 'read-only')

        if self.changes['user'].get('passwd') is None:
            # user name
            name = self.changes['user']['name']

            # ask password
            passwd = getpass.getpass(f'{name} password: ')

            # update local db
            self.changes['user'].update(passwd=passwd)

    def run(self):
        """Start task."""
        # get password
        passwd = self.changes['user']['passwd']

        # get pasword hash to send over the wire
        passwd_hash = secure_hash(passwd)

        # command arguments
        kwargs = self.changes['user'].copy()
        kwargs['encrypted_passwd'] = passwd_hash

        self.dev.cu.load(self.command_mask.format(**kwargs))
        self.dev.cu.commit()