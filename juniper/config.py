"""Parses yaml configuration files."""

from typing import Any

import yaml


class ErrorBag(TypeError):
    """Hold required keys missing in configuration."""

    def __init__(self, keys: list) -> None:
        """Instantiate parent class with a builtin fail message."""
        keys_str =  ', '.join(keys)
        super().__init__(f'Missing required fields inside config: {keys_str}')
        self.keys = keys


def read(file_path: str) -> dict:
    """Read yaml configuration and ensure has required fields."""
    config = read_yaml(file_path)

    # lookup for missing fields 
    missing_fields = collect_missing_fields(config)

    if missing_fields:
        raise ErrorBag(missing_fields)

    return config


def read_yaml(file_path: str) -> dict:
    """Read yaml file into a dictionary."""
    with open(file_path, 'rb') as f_reader:
        return yaml.safe_load(f_reader)


def collect_missing_fields(config: dict) -> list:
    """
    Return list of missing required fields.

    When `config` is valid, should return an empty list.
    """
    fields = ['ssh.host', 
              'changes.user.name', 
              'changes.banner',
              'changes.config',]

    # pre-process all information possible
    ssh_cfg = config.get('ssh', {})
    changes_cfg = config.get('changes', {})

    ## check `ssh.host`
    if ssh_cfg.get('host'):
        fields.remove('ssh.host')

    ## check `changes.user.name`
    if changes_cfg.get('user', {}).get('name'):
        fields.remove('changes.user.name')

    ## check `changes.banner`
    if changes_cfg.get('banner') or changes_cfg.get('banner_file'):
        fields.remove('changes.banner')

    ## check `changes.config`
    if changes_cfg.get('config') or changes_cfg.get('config_file'):
        fields.remove('changes.config')

    return fields