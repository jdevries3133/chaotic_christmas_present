import os
from pathlib import Path

from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class MarkdownSlugPathValidator:

    def __init__(self, slug):
        self.slug = slug
        self.validated = False

    def get_path(self):
        if self.validated:
            return self._slug_to_path()
        raise Exception(
            "You may not call get_slug before first calling is_valid()"
        )

    def is_valid(self) -> bool:
        """
        Return true if the path is valid, or raise a validation error if not.
        """
        if os.path.exists(
            Path(
                settings.BASE_DIR,
                'staff',
                'markdown',
                self._slug_to_path()
            )
        ):
            self.validated = True
            return True
        raise ValidationError(_('Invalid URL'))

    def _slug_to_path(self):
        """
        Convert slug to a filesystem path.
        """
        parts = self.slug.split('.')
        return Path(
            '/'.join(parts[:-2]) + '/' + '.'.join(parts[-2:])
        )
