"""Test `juniper.task.abc` module."""


from juniper.task import abc


class DummyTask(abc.AbstractTask): # noqa disable=D101
    def run(self):  # noqa disable=D102
        pass


def test_abstract_task_exposes_public_props(mock_factory):
    """Abstract class exposes configuration and device properties."""
    device = mock_factory()
    config = dict(foo='bar')

    task = DummyTask(device, config)

    assert task.dev == device
    assert task.config == config
    assert task.changed is False
