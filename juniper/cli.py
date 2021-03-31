"""Interface functions for starting the application."""

import os
import sys

from jnpr.junos import Device

# environment variable of configuration file
CONFIG_ENV_NAME = 'JNPR_CONFIG_FILE'


def deduce_config_file() -> str:
    """Return file path of configuration file when any."""
    if len(sys.argv) > 1:
        return sys.argv[1]

    config_file = os.getenv(CONFIG_ENV_NAME)
    if not config_file:
        raise TypeError('Missing configuration file parameter.')

    return config_file


def main():
    """Entrypoint for script interaction."""
    pass


def make_device(config: dict) -> Device:
    """Return a juniper device from configuration."""
    ssh_cfg = config['ssh']

    kwargs = {
        'host': ssh_cfg['host'],
        'ssh_config': ssh_cfg.get('config'),
        'port': 22,
    }

    return Device(**kwargs)