from django.test import TestCase
from django.test import Client

# Create your tests here.
class TestFormVulnerability(TestCase):
    def test_form_executes_query(self):
        client = Client()
        with self.assertNumQueries(1):
            client.post('/contact/', {
                'subject': 'any',
                'message': 'SELECT name from SQLITE_MASTER;',
            })


