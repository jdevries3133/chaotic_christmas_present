from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.db import connection
from django.test import Client

from .models import ContactFormData

# Create your tests here.
class TestFormVulnerability(TestCase):

    def test_form_executes_query(self):
        client = Client()
        with self.assertNumQueries(1):
            client.post('/contact/', {
                'subject': 'any',
                'message': 'SELECT name from SQLITE_MASTER;',
            })

    def test_form_works_with_normal_use(self):
        """
        Naive "expected" behavior is for database insertion to happen
        unconsequentially if an SQL injection attack is not attempted.
        """
        client = Client()
        client.post('/contact/', {
            'subject': 'foo',
            'message': 'bar',
        })
        self.assertTrue(ContactFormData.objects.filter(subject='foo', message='bar'))

    def test_custom_query_mimics_orm(self):
        with CaptureQueriesContext(connection) as ctx:
            orm_query = 'INSERT INTO "sql_vulnerable_contactformdata" ("subject", "message") VALUES (\'a\', \'b\')'
            client = Client()
            client.post('/contact/', {
                'subject': 'foo',
                'message': 'bar',
            })
            query = "INSERT INTO sql_vulnerable_contactformdata (subject, message) VALUES ('foo', 'bar');"
            self.assertTrue(query in [i['sql'] for i in ctx.captured_queries])
