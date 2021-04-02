"""Load arbitrary configuration with Jinja2 template engine."""


import os
import tempfile

from . import abc, utils


class CfgTemplateTask(abc.AbstractTask):
    """Load templates with Juno facts."""

    def pre_start(self) -> None:
        """Ensure `config_file` exists when should use it."""
        if self.use_config_file():
            utils.file_or_fail(self.changes['config_file'])

    def run(self) -> None:
        """Start task."""
        if self.use_config_file():
            template_path = self.changes['config_file']
        else:
            # create a temp file to store text
            template_path = tempfile.mkstemp()[1]

            # write `config` to file
            with open(template_path, 'w') as fp:
                fp.write(self.changes['config'])

        # gather facts
        facts = self.dev.facts

        self.dev.cu.load(template_path=template_path,
                         template_vars=facts)

        self.dev.cu.commit()

        if not self.use_config_file():
            try:
                os.unlink(template_path)
            except Exception as exc:
                print(exc)

    def use_config_file(self) -> bool:
        """Return whether should use `config_file`."""
        return not self.changes.get('config')