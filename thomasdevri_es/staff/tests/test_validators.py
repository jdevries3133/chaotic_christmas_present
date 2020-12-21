from pathlib import Path

from django.core.exceptions import ValidationError

from .base_test_cases import BaseMarkdownFilesystemTest
from ..validators import MarkdownSlugPathValidator


class TestMarkdownSlugPathValidator(BaseMarkdownFilesystemTest):

    def test_valid_paths_raise_no_exception(self):
        with self.settings(BASE_DIR=self.testdir):
            for path in self.mock_markdown_paths:
                slug = str(path).replace('/', '.')
                validator = MarkdownSlugPathValidator(slug)
                self.assertTrue(validator.is_valid())

    def test_conversion(self):
        with self.settings(BASE_DIR=self.testdir):
            path = MarkdownSlugPathValidator('c.c.c.c1.md')._slug_to_path()
            self.assertEqual(path, Path('c', 'c', 'c', 'c1.md'))

    def test_invalid_paths_are_rejected(self):
        test_slugs = [
            'etc.passwd',
            'a.a.a1.html',
            'b.c.env',
            'a.a1.txt'
        ]
        with self.settings(BASE_DIR=self.testdir):
            for slug in test_slugs:
                path = MarkdownSlugPathValidator(slug)
                with self.assertRaises(ValidationError):
                    path.is_valid()

    def test_premature_get_slug_raises_exception(self):
        with self.settings(BASE_DIR=self.testdir):
            with self.assertRaises(Exception):
                MarkdownSlugPathValidator('foo').get_path()
