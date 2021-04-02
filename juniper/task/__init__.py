"""Provide implementations to handle specific actions with Junos device."""


from typing import List

from . import abc, banner, ssh_passwd, template, user

# hold default tasks allowed to run.
registered_ones = [
    ssh_passwd.SSHPassword,
    banner.BannerTask,
    user.UserMgmtTask,
    template.CfgTemplateTask,
]


def load_list() -> List[abc.AbstractTask]:
    """Return a list of all available tasks."""
    return registered_ones.copy()
