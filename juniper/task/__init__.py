"""Provide implementations to handle specific actions with Junos device."""


from typing import List

from . import abc, banner, ssh_passwd

# hold default tasks allowed to run.
registered_ones = [
    ssh_passwd.SSHPassword,
    banner.BannerTask,
]


def load_list() -> List[abc.AbstractTask]:
    """Return a list of all available tasks."""
    return registered_ones.copy()
