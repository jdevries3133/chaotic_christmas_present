import os
from pathlib import Path

from django.conf import settings


class MarkdownSlugPathValidator:
    """
    Validates that a markdown directory path passed in as a slug exists before
    proceeding.
    """

    def __init__(self, slug: str, markdown_root: Path):
        self.slug = slug
        self.markdown_root = markdown_root
        self.validated = False

    def get_path(self):
        if self.validated:
            return self._slug_to_path()
        raise Exception(
            "You may not call get_path on an invalid or unvalidated slug"
        )

    def is_valid(self) -> bool:
        """
        Return true if the path is valid, or raise a validation error if not.
        """
        if os.path.exists(
            Path(
                self.markdown_root,
                self._slug_to_path()
            )
        ):
            self.validated = True
            return True
        return False

    def _slug_to_path(self):
        """
        Convert slug to a filesystem path.
        """
        parts = self.slug.split('.')
        if len(parts) == 1:
            return Path(self.markdown_root, self.slug + '.md')
        return Path(
            self.markdown_root,
            '/'.join(parts) + '.md'
        )
