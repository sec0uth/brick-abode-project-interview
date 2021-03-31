"""Test `juniper.config` module."""


import yaml
from pathlib import Path

import pytest
from juniper import config


def test_read_from_file(cfg_template):
    """Read yaml file and return a dict."""
    result = config.read(cfg_template)
    assert type(result) is dict


def test_succeed_to_validate_required_fields(monkeypatch, tmp_path):
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
            'banner_file': 'something',

            'user': {
                'name': 'bar',
            },

            'config': dummy_file.name,
        },
    }

    datasets_to_ret = [dataset_v1,
                       dataset_v2,
                       dataset_v3,]

    def yaml_load_patch(*_, **__):
        return datasets_to_ret.pop()

    # patch yaml to return expected
    monkeypatch.setattr(yaml, 'load', yaml_load_patch)

    # loop the size of the datasets and 
    # validate the dataset input
    for _ in datasets_to_ret:
        try:
            config.read(dummy_file)
        except:
            pytest.fail()
