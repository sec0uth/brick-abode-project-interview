"""Parses yaml configuration files."""


import yaml


class ErrorBag(TypeError):
    """Hold required keys missing in configuration."""

    def __init__(keys: list) -> None:
        """Instantiate parent class with a builtin fail message."""
        keys_str =  ', '.join(keys)
        super().__init__(f'Missing required fields inside config: {key_str}')
        self.key = keys


def read(file_path: str) -> dict:
    """Read yaml file into a dictionary."""
    with open(file_path, 'rb') as f_reader:
        return yaml.safe_load(f_reader)