from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.urls import reverse


from .base_test_cases import (
    BaseTestWithStaffUser,
    BaseMarkdownFilesystemTest
)

class TestLoginView(BaseTestWithStaffUser):

    def test_login_view_get_request(self):
        self.client.get(reverse('staff_login'))

    def test_staff_login_view_empty_post_request(self):
        self.client.post(reverse('staff_login'))

    def test_staff_login_view_authenticates_user(self):
        response = self.client.post(
            reverse('staff_login'),
            {
                'username': self.username,
                'password': self.password,
            }
        )
        self.assertRedirects(response, reverse('dashboard'))



class TestDocumentationView(BaseTestWithStaffUser, BaseMarkdownFilesystemTest):

    def test_invalid_slug_renders_not_found_template(self):
        provided_slug = 'invalid'
        url = reverse(
            'documentation',
            kwargs={
                'markdownslug': provided_slug
            }
        )
        response = self.client.get(url)

        # not found template is used
        self.assertTemplateUsed(response, 'staff/docs/not_found.html')
        # bad slug is in the context
        self.assertTrue(context_slug := response.context.get('bad_slug'))  # type: ignore
        # bad slug is same as provided slug
        self.assertEqual(context_slug, provided_slug)

    def test_valid_slug_renders_markdown(self):
        """
        TODO
        """
        raise NotImplementedError
