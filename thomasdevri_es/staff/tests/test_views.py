from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.urls import reverse


from .base_test_cases import (
    BaseTestWithStaffUser,
    BaseMarkdownFilesystemTest
)

class TestLoginView(TestCase):

    def setUp(self):
        self.username = 'thisisatestusernamethatislong'
        self.password = 'fdsahifhsaudfireua9eaighueaar3ww2w'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            is_staff=True,
        )
        self.client = Client()

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

    def test_test(self):
        pass
