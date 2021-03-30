"""Parses yaml configuration files."""


import yaml


def read(file_path: str) -> dict:
    """Read yaml file into a dictionary."""
    with open(file_path, 'rb') as f_reader:
        return yaml.safe_load(f_reader)