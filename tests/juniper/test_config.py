"""Test `juniper.config` module."""


import yaml
from pathlib import Path

import pytest
from juniper import config


def test_read_from_file(cfg_template):
    """Read yaml file and return a dict."""
    result = config.read(cfg_template)
    assert type(result) is dict


def test_succeed_to_validate_logging(monkeypatch, tmp_path):
    """Succeeds to read valid yaml configurations."""
    # contains variations of console and verbose
    # characterists, but file is None
    return_dataset1 = [
        [True, True, None],
        [True, False, None],
        [False, True, None],
        [False, False, None],
    ]

    # add combinations with a file as string
    return_dataset2 =  [returnopts for returnopts in return_dataset1
                        if returnopts.insert(2, 'foo')]


    logging_to_ret =  return_dataset1 + return_dataset2

    def load_effect(*_, **__):
        dataset = logging_to_ret.pop()

        return {
            'logging': {
                'console': dataset[0],
                'verbose': dataset[1],
                'file': dataset[2],
            },
        }


    # patch yaml to return expected
    monkeypatch.setattr(yaml, 'load', load_effect)

    # create dummy file in temporary dir
    file_path = tmp_path / Path('bar.foo')
    file_path.write_bytes(b'')

    # loop the size of the datasets and 
    # validate the dataset input
    for _ in logging_to_ret:
        try:
            config.read(file_path)
        except:
            pytest.fail()
