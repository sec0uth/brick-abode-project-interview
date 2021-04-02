"""Load arbitrary configuration with Jinja2 template engine."""


from . import abc


class CfgTemplateTask(abc.AbstractTask):
    """Load templates with Juno facts."""

    def pre_start(self) -> None:
        """Ensure `config_file` exists when should use it."""
        pass

    def run(self) -> None:
        """Start task."""