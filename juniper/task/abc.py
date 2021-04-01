"""Abstract classes related to task management."""


from abc import ABC, abstractmethod

from jnpr.junos import Device
from jnpr.junos.utils import Util


class AbstractTask(ABC, Util):
    """Abstraction layer for creating a task on Juniper devices."""

    def __init__(self, device: Device, config: dict) -> None:
        """Class constructor."""
        super().__init__(device)
        self.config = config
        self._changed = False

    @abstractmethod
    def run(self) -> None:
        """Start task."""
        pass

    def pre_start(self) -> None:
        """
        Initialize task before actually starting it.
        
        Subclasses may override this method. 
        """
        pass

    @property
    def changed(self) -> bool:
        """Return whether task applied changes to device."""
        return self._changed

    @property
    def changes(self) -> dict:
        """Return `changes` section of `config` property."""
        return self.config['changes']

    def _set_changed(self) -> None:
        """Set task changed the device."""
        self._changed = True