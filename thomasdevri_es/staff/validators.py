import os
from pathlib import Path

from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class MarkdownSlugPathValidator:

    def __init__(self, slug):
        self.slug = slug

    def _slug_to_path(self):
        """
        Convert slug to a filesystem path.
        """
        parts = self.slug.split('.')
        return Path(
            '/'.join(parts[:-2]) + '/' + '.'.join(parts[-2:])
        )

    def is_valid(self) -> bool:
        if os.path.exists(
            Path(
                settings.BASE_DIR,
                'staff',
                'markdown',
                self._slug_to_path()
            )
        ):
            return True
        raise ValidationError(_('Invalid URL'))
