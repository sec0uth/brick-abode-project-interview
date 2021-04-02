"""Task to change the banner."""

from jnpr.junos.utils.config import Config

from . import abc, utils


class BannerTask(abc.AbstractTask):
    """Change Juniper banner from configuration."""

    # Juno command to edit login banner
    command_mask = 'set system login message "{content}"'

    def pre_start(self) -> None:
        """Ensure `banner_file` exists when using it."""
        if self.use_banner_file():
            utils.file_or_fail(self.changes['banner_file'])

    def run(self) -> None:
        """Start task."""
        # take `banner` by default
        raw_content = self.changes.get('banner')

        # when `banner` is empty, get `banner_file` contents
        if not raw_content:
            with open(self.changes['banner_file']) as fp:
                raw_content = fp.read()

        # clean content
        content = raw_content.strip()

        self.dev.cu.load(self.command_mask.format(content=content))
        self.dev.cu.commit()
    
    def use_banner_file(self) -> bool:
        """Return whether task should use `banner_file`."""
        return not self.changes.get('banner')

