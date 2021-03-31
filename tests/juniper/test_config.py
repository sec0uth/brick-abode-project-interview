"""Test `juniper.config` module."""


from pathlib import Path

import pytest
import yaml

from juniper import config


def test_read_from_file(cfg_template):
    """Read yaml file and return a dict."""
    result = config.read(cfg_template)
    assert isinstance(result, dict)


def test_succeed_to_validate_required_fields(monkeypatch, 
                                             tmp_path,
                                             mock_factory):
    """Succeeds to read valid yaml configurations."""
    # create dummy file in temporary dir
    dummy_file = tmp_path / Path('bar.foo')
    dummy_file.write_bytes(b'')

    # with `banner` and `config`
    dataset_v1 = {
        'ssh': {
            'host': 'foo',
        },
        'changes': {
            'banner': 'something',

            'user': {
                'name': 'bar',
            },

            'config': 'any',
        },
    }

    # with `config` and `banner_file`
    dataset_v2 = {
        'ssh': {
            'host': 'foo',
        },
        'changes': {
            'banner_file': dummy_file.name,

            'user': {
                'name': 'bar',
            },

            'config': 'any',
        },
    }

    # with `config_file` and `banner`
    dataset_v3 = {
        'ssh': {
            'host': 'foo',
        },
        'changes': {
            'banner': 'something',

            'user': {
                'name': 'bar',
            },

            'config_file': dummy_file.name,
        },
    }

    # with `config_file` and `banner_file`
    dataset_v4 = {
        'ssh': {
            'host': 'foo',
        },
        'changes': {
            'banner_file': dummy_file.name,

            'user': {
                'name': 'bar',
            },

            'config_file': dummy_file.name,
        },
    }

    datasets_to_ret = [dataset_v1,
                       dataset_v2,
                       dataset_v3,
                       dataset_v4,]

    # `side_effect` instruct the mock to return one
    # element of `datasets_to_ret` each time is called
    patch_fn = mock_factory(side_effect=datasets_to_ret)

    # patch yaml to return each dataset at time
    monkeypatch.setattr(yaml, 'load', patch_fn)

    # loop the size of the datasets and 
    # validate the dataset input
    for _ in datasets_to_ret:
        try:
            config.read(dummy_file)
        except:
            pytest.fail()


def test_fail_validate_without_any_required_fields(monkeypatch, 
                                                   tmp_path,
                                                   mock_factory):
    """Fail to read config with missing required fields."""
    expected_fields = ['ssh.host', 
                       'changes.user.name', 
                       'changes.banner',
                       'changes.config',]

     # empty
    dataset = {}

    patch_fn = mock_factory(return_value=dataset)

    # patch yaml to return expected
    monkeypatch.setattr(yaml, 'load', patch_fn)

    # create dummy file in temporary dir
    dummy_file = tmp_path / Path('bar.foo')
    dummy_file.write_bytes(b'')

    with pytest.raises(config.ErrorBag) as exc_manager:
        config.read(dummy_file)

    missing_fields = exc_manager.value.keys 

    assert missing_fields == expected_fields

