"""Test `juniper.task.utils` module."""

import hashlib
from datetime import datetime
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


## name_for_backup()
#################################


def test_handle_absolute_path_with_extension(now_mock):
    """Format absolute file path with an extension."""
    name = '/foo/bar.baz'
    expected_name = '/foo/bar-1789-12-21T04-02.baz'

    expected_datetime = datetime(year=1789, 
                                 month=12, 
                                 day=21, 
                                 hour=4, 
                                 minute=2)

    now_mock.return_value = expected_datetime

    result = utils.name_for_backup(name)

    assert result == expected_name


def test_handle_no_extension(now_mock):
    """Format absolute file path with an extension."""
    name = '/foo/bar'
    expected_name = f'{name}-1789-12-21T04-02'

    expected_datetime = datetime(year=1789, 
                                 month=12, 
                                 day=21, 
                                 hour=4, 
                                 minute=2)

    now_mock.return_value = expected_datetime

    result = utils.name_for_backup(name)

    assert result == expected_name