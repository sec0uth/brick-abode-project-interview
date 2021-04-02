"""Interface functions for starting the application."""

import os
import sys

from jnpr.junos import Device
from jnpr.junos.utils.config import Config

from . import config, task

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


def main() -> int:
    """Entrypoint for script interaction."""
    config_file = deduce_config_file()

    configuration = config.read(config_file)

    juno_dev = make_device(configuration)
    
    # hold tasks objects
    task_store = []

    # create a config copy for tasks classes
    task_config = configuration.copy()

    # setup tasks
    for task_class in task.load_list():
        # instantiate task object
        task_obj = task_class(juno_dev, task_config)

        # make any preparation
        task_obj.pre_start()

        # save it
        task_store.append(task_obj)

    # run each task with device connected
    with juno_dev as connected_dev:
        with Config(connected_dev) as cu:
            # trick to bind an existing object
            connected_dev.bind(cu=lambda _: cu)
            
            for task_obj in task_store:
                task_obj.run()

    return 0


def make_device(config: dict) -> Device:
    """Return a juniper device from configuration."""
    ssh_cfg = config['ssh']

    kwargs = {
        'host': ssh_cfg['host'],
        'ssh_config': ssh_cfg.get('config'),
        'port': 22,
    }

    return Device(**kwargs)