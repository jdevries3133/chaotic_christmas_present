from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.db import connection
from django.test import Client

from .models import ContactFormData
from .init import init_data

# TODO: group tests by common setups

# Create your tests here.
class TestFormVulnerability(TestCase):

    def setUp(self):
        for _ in range(10):
            ContactFormData.objects.create(  # type: ignore
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
        response = client.post('/contact/', {
            'subject': 'foo',
            'message': 'bar',
        })
        self.assertTrue(
            ContactFormData.objects.filter(  # type: ignore
                subject='foo',
                message='bar'
            )
        )
        self.assertEqual(
            response.context['real_data']['subject'],  # type: ignore
            'foo',
        )
        self.assertEqual(
            response.context['real_data']['message'],  # type: ignore
            'bar',
        )

    def test_custom_query_mimics_orm(self):
        with CaptureQueriesContext(connection) as ctx:
            client = Client()
            client.post('/contact/', {
                'subject': 'foo',
                'message': 'bar',
            })
            orm_query = (
                "INSERT INTO sql_vulnerable_contactformdata (subject, message) "
                "VALUES ('foo', 'bar')"
            )
            self.assertIn(
                orm_query, [
                    i['sql'] for i in ctx.captured_queries
                ]
            )

    def test_sql_injection_successful(self):
        client = Client()
        injected_query = 'SELECT * FROM sql_vulnerable_contactformdata'
        with CaptureQueriesContext(connection) as ctx:
            client.post('/contact/', {
                'subject': 'foo',
                'message': (
                    'bar\'); SELECT * FROM sql_vulnerable_contactformdata; '
                ),
            })
            self.assertIn(
                injected_query, [
                    i['sql'].strip() for i in ctx.captured_queries
                ]
            )

    def test_sql_query_results_passed_to_template_context(self):
        client = Client()
        response = client.post('/contact/', {
            'subject': 'foo',
            'message': (
                'bar\'); SELECT * FROM sqlite_master; '
            ),
        })
        with connection.cursor() as cursor:
            expected_db_response = cursor.execute(
                'SELECT * FROM sqlite_master'
            ).fetchall()
        query_responses = response.context.get('query_responses')  # type: ignore
        for i in expected_db_response:
            self.assertIn(i, query_responses)

class TestInit(TestCase):
    """
    Ensure that the initialization script runs and inserts hidden data for
    thomas to find.

    main() of sql_vulnerable.init is imported as init_data
    """
    def test_runs_without_exceptions(self):
        init_data()

    def test_data_exists_in_db(self):
        pass
