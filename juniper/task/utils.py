"""Utility functions for tasks to use."""

import datetime
import hashlib
import os


def file_checksum(file_path: str) -> str:
    """Return hash sum of `file_path` using SHA256 algorithm."""
    with open(file_path, 'rb') as fp:
        bytes_content = fp.read()

    # instantiate algorithm of hashsum
    hash_algo = hashlib.sha256()

    # add bytes of interest
    hash_algo.update(bytes_content)

    return hash_algo.hexdigest()


def name_for_backup(file_path: str) -> str:
    """
    Return how a file backup would looks like.
    
    Examples:
        >>> name_for_backup('/var/log/auth.log')
        /var/log/auth-2021-04-01T22-00.log
    """
    name, extension = os.path.splitext(file_path)

    # remove trailing dash
    name = name.rstrip('-')

    # snapshot datetime
    now = datetime.datetime.now()

    # format datetime to a valid file name format
    time_id = now.strftime('%Y-%m-%dT%H-%M')

    return f'{name}-{time_id}{extension}'


def file_or_fail(file_path: str) -> None:
    """
    Fail when `file_path` is not an existing file.

    Raise `FileNotFoundError` when does not exists in file system. 
    Then, may raise `ValueError` if not is a file. 
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    if not os.path.isfile(file_path):
        raise ValueError(f'Argument not a file at: {file_path}')
        