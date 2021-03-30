"""Test `juniper.config` module."""


from juniper import config


def test_read_from_file(cfg_template):
    """Read yaml file and return a dict."""
    result = config.read(cfg_template)
    assert type(result) is dict
