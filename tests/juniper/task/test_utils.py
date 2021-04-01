"""Test `juniper.task.utils` module."""

import hashlib
from pathlib import Path

from juniper.task import utils


## file_checksum()
#################################


def test_calculate_correct_sum(tmp_path):
    """Calculate the same checksum of the string in the file."""
    content = b'foo bar baz'

    # calculate `content` checksum at runtime
    hash_algo = hashlib.sha256()
    hash_algo.update(content)
    expected_sha256sum = hash_algo.hexdigest()

    # write content down
    target_file = tmp_path / Path('test.file')
    target_file.write_bytes(content)

    result = utils.file_checksum(target_file)

    assert result == expected_sha256sum 
