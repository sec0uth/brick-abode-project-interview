"""Provide implementations to handle specific actions with Junos device."""


from typing import List

from . import abc

# hold default tasks allowed to run.
registered_ones = [

]


def load_list() -> List[abc.AbstractTask]:
    """Return a list of all available tasks."""
    return registered_ones.copy()
