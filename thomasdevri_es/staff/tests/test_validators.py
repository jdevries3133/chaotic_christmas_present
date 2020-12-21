from pathlib import Path

from django.core.exceptions import ValidationError

from .base_test_cases import BaseMarkdownFilesystemTest
from ..validators import MarkdownSlugPathValidator


class TestMarkdownSlugPathValidator(BaseMarkdownFilesystemTest):

    def test_valid_paths_raise_no_exception(self):
        with self.settings(BASE_DIR=self.testdir):
            for path in self.mock_markdown_paths:
                slug = str(path.relative_to(self.markdown_root))[:-3].replace('/', '.')
                validator = MarkdownSlugPathValidator(slug, self.markdown_root)
                self.assertTrue(validator.is_valid())

    def test_conversion(self):
        with self.settings(BASE_DIR=self.testdir):
            for path in self.mock_markdown_paths:
                slug = str(path.relative_to(self.markdown_root))[:-3].replace('/', '.')
                validator = MarkdownSlugPathValidator(
                    slug,
                    self.markdown_root
                )
                new_path = validator._slug_to_path()
                self.assertEqual(
                    path.resolve(),
                    new_path.resolve(),
                )

    def test_invalid_paths_are_rejected(self):
        test_slugs = [
            'etc.passwd',
            'a.a.a1.html',
            'b.c.env',
            'a.a1.txt'
        ]
        with self.settings(BASE_DIR=self.testdir):
            for slug in test_slugs:
                path = MarkdownSlugPathValidator(slug, self.markdown_root)
                self.assertFalse(path.is_valid())

    def test_premature_get_slug_raises_exception(self):
        with self.settings(BASE_DIR=self.testdir):
            with self.assertRaises(Exception):
                MarkdownSlugPathValidator('foo', self.markdown_root).get_path()
