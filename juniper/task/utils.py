"""Utility functions for tasks to use."""

import hashlib


def file_checksum(file_path: str) -> str:
    """Return hash sum of `file_path` using SHA256 algorithm."""
    with open(file_path, 'rb') as fp:
        bytes_content = fp.read()

    # instantiate algorithm of hashsum
    hash_algo = hashlib.sha256()

    # add bytes of interest
    hash_algo.update(bytes_content)

    return hash_algo.hexdigest()