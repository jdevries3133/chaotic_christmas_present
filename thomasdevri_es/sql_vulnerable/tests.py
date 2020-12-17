from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.db import connection
from django.test import Client

from .models import ContactFormData

# Create your tests here.
class TestFormVulnerability(TestCase):

    def setUp(self):
        for _ in range(10):
            ContactFormData.objects.create(
                subject='setup subject',
                message='setup message',
            )

    def test_form_executes_query(self):
        client = Client()
        with self.assertNumQueries(1):
            client.post('/contact/', {
                'subject': 'foo',
                'message': 'bar',
            })

    def test_form_works_with_normal_use(self):
        client = Client()
        client.post('/contact/', {
            'subject': 'foo',
            'message': 'bar',
        })
        self.assertTrue(ContactFormData.objects.filter(subject='foo', message='bar'))  # type: ignore

    def test_custom_query_mimics_orm(self):
        with CaptureQueriesContext(connection) as ctx:
            client = Client()
            client.post('/contact/', {
                'subject': 'foo',
                'message': 'bar',
            })
            orm_query = "INSERT INTO sql_vulnerable_contactformdata (subject, message) VALUES ('foo', 'bar')"
            self.assertTrue(orm_query in [i['sql'] for i in ctx.captured_queries])

    def test_sql_injection_successful(self):
        client = Client()
        injected_query = 'SELECT * FROM sql_vulnerable_contactformdata'
        with CaptureQueriesContext(connection) as ctx:
            client.post('/contact/', {
                'subject': 'foo',
                'message': 'bar\'); SELECT * FROM sql_vulnerable_contactformdata; ',
            })
            self.assertTrue(injected_query in [i['sql'].strip() for i in ctx.captured_queries])
