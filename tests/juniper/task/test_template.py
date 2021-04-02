"""Test `juniper.task.template` module."""

import tempfile
from pathlib import Path

import pytest

from juniper.task import template


@pytest.fixture
def task(mock_factory):
    """Return instance of `juniper.task.template.CfgTemplateTask`."""
    default_config = {
        'changes': {
            'config': 'set foo bar',
            'config_file': 'baz',
        },
    }

    return template.CfgTemplateTask(mock_factory(), default_config)


## CfgTemplateTask.run()
#################################


def test_load_and_commit_configuration_finally(task):
    """Manage configuration with a load and a commit."""
    # trigger
    task.run()

    task.dev.cu.load.assert_called_once()
    task.dev.cu.commit.assert_called_once()


def test_prioritize_config_text(task):
    """Use `config` instead of `config_file` when have both."""
    # trigger
    task.run()

    call_kwargs = task.dev.cu.load.call_args[1]

    assert call_kwargs['template_path'] != task.changes['config_file']


def test_load_template_with_facts(task):
    """Load template using facts as `template_vars`."""
    expected_facts = {
        'i': 'amdumb'
    }

    # patch gathering facts
    task.dev.facts = expected_facts

    # trigger
    task.run()

    call_kwargs = task.dev.cu.load.call_args[1]

    assert call_kwargs['template_vars'] == expected_facts


def test_load_template_with_temporary_file(task, 
                                           monkeypatch,
                                           mock_factory,
                                           tmp_path):
    """Load template using a temporary file with `config`."""
    expected_path = tmp_path / Path('baz.tmp')

    # tuple with some file descriptor and the file path
    mkstemp_ret = (1, expected_path)

    monkeypatch.setattr(tempfile, 
                        'mkstemp', 
                        mock_factory(return_value=mkstemp_ret))

    # trigger
    task.run()

    call_kwargs = task.dev.cu.load.call_args[1]

    assert call_kwargs['template_path'] == expected_path


def test_load_template_with_text(task, 
                                 monkeypatch,
                                 mock_factory,
                                 tmp_path):
    """Load template using a temporary file to store `config` text."""
    dummy_file = tmp_path / Path('template.j2')

    # tuple with some file descriptor and the file path
    mkstemp_ret = (1, dummy_file)

    monkeypatch.setattr(tempfile, 
                        'mkstemp', 
                        mock_factory(return_value=mkstemp_ret))

    # trigger
    task.run()

    assert dummy_file.read_text() == task.changes['config']


def test_load_template_with_config_file(task):
    """Load template using `config_file`."""
    # disable `config`
    task.changes.update(config=None)

    # trigger
    task.run()

    call_kwargs = task.dev.cu.load.call_args[1]

    assert call_kwargs['template_path'] == task.changes['config_file']


## CfgTemplateTask.pre_start()
#################################


def test_fail_with_invalid_config_file(task, tmp_path):
    """Fail with an invalid config file."""
    missing_file = tmp_path / Path('missing.txt')

    task.changes.update(config=None,
                        config_file=missing_file)

    with pytest.raises(FileNotFoundError):
        task.pre_start()

    
def test_succeed_with_valid_config_file(task, tmp_path):
    """Succeed with a valid config file."""
    valid_file = tmp_path / Path('template.j2')
    valid_file.write_text('')

    task.changes.update(config=None,
                        config_file=valid_file)

    task.pre_start()


def test_succeed_with_invalid_config_file(task, tmp_path):
    """Succeed with an invalid config file when has `config`."""
    missing_file = tmp_path / Path('missing.txt')

    task.changes.update(config_file=missing_file)

    task.pre_start()