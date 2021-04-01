"""Task to change the banner."""

from jnpr.junos.utils.config import Config

from . import abc, utils


class BannerTask(abc.AbstractTask):
    """Change Juniper banner from configuration."""

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

        # apply configuration change
        with Config(self.dev) as cu:
            cu.load(f'set system login message "{content}"', format='set')
            cu.commit()
    
    def use_banner_file(self) -> bool:
        """Return whether task should use `banner_file`."""
        return not self.changes.get('banner')

