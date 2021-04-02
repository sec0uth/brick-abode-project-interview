"""Test `juniper.task.banner` module."""

from pathlib import Path

import pytest

from juniper.task import banner


class MockCtxManager:
    """Return arbitrary objects as context manager."""

    def __init__(self, return_value):   # noqa disable=D107
        self.return_value = return_value

    def __enter__(self, *_, **__):  # noqa disable=D105
        return self.return_value

    def __exit__(self, *_, **__):   # noqa disable=D105
        pass


@pytest.fixture(scope='function')
def task(mock_factory):
    """Return a new banner task."""
    default_config = {
        'changes': {
            'banner': 'foo',
            'banner_file': 'baz',
        }
    }

    return banner.BannerTask(mock_factory(), default_config)


def test_commits_configuration_finally(task):
    """Commit configuration when changed."""
    # trigger
    task.run()

    task.dev.cu.commit.assert_called_once()


def test_prioritize_banner_message(task):
    """Use `banner` instead of `banner_file` when have both."""
    expected_msg = '@banner foo@'

    task.changes.update(banner=expected_msg)

    # trigger
    task.run()

    task.dev.cu.load.assert_called_once()

    # ensure called `load()` with `banner`
    call_first_arg = task.dev.cu.load.call_args[0][0]
    assert expected_msg in call_first_arg


def test_read_banner_from_file(task, tmp_path):
    """Use `banner_file` when `banner` is missing."""
    expected_msg = '!banner from file!'

    dummy_file = tmp_path / Path('banner.txt')
    dummy_file.write_text(expected_msg)
    
    # disable `banner` and set `banner_file`
    task.changes.update(banner=None, 
                        banner_file=dummy_file)

    # trigger
    task.run()

    task.dev.cu.load.assert_called_once()

    # ensure called `load()` with `banner`
    call_first_arg = task.dev.cu.load.call_args[0][0]
    assert expected_msg in call_first_arg


def test_clean_banner_message_new_lines(task):
    """Remove trailing/leading new line chars."""
    dirty_msg = '\n\nfoo\n\n\n'

    task.changes.update(banner=dirty_msg)

    # trigger
    task.run()

    task.dev.cu.load.assert_called_once()

    # ensure called with cleaned version of banner
    call_first_arg = task.dev.cu.load.call_args[0][0]
    assert dirty_msg not in call_first_arg


def test_fail_with_invalid_banner_file(task, tmp_path):
    """Fail on `pre_start()` with an invalid banner file."""
    missing_file = tmp_path / Path('missing.txt')

    task.changes.update(banner=None,
                        banner_file=missing_file)

    with pytest.raises(FileNotFoundError):
        task.pre_start()

    
def test_succeed_with_valid_banner_file(task, tmp_path):
    """Succeed on `pre_start()` with an valid banner file."""
    valid_file = tmp_path / Path('banner.txt')
    valid_file.write_text('')

    task.changes.update(banner=None,
                        banner_file=valid_file)

    task.pre_start()


def test_succeed_with_invalid_banner_file(task, tmp_path):
    """Succeed on `pre_start()` with an invalid banner file when has `banner`."""
    missing_file = tmp_path / Path('missing.txt')

    task.changes.update(banner_file=missing_file)

    task.pre_start()
