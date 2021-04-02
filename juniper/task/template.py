"""Load arbitrary configuration with Jinja2 template engine."""


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

            self.load_and_commit(template_path)
        else:
            with tempfile.NamedTemporaryFile() as tmp_file:
                text_bytes = self.changes['config'].encode('utf-8')

                # write `config` to file
                tmp_file.write(text_bytes)

                # have to force pushing data to disk,
                # otherwise Jinja doesn't have time to read
                tmp_file.flush()

                self.load_and_commit(tmp_file.name)

    def load_and_commit(self, template_path: str) -> None:
        """Manage loading and commiting template."""
        # gather facts
        facts = self.dev.facts

        self.dev.cu.load(template_path=template_path,
                         template_vars=facts,
                         format='set')

        self.dev.cu.commit()

    def use_config_file(self) -> bool:
        """Return whether should use `config_file`."""
        return not self.changes.get('config')