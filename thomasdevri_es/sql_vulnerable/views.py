import logging

from django.shortcuts import render
from django.db import connection
from django.db.utils import OperationalError

from sql_vulnerable.models import ContactFormData  # type: ignore

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'sql_vulnerable/home.html')

def formpage(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            query = (
                'INSERT INTO sql_vulnerable_contactformdata '
                f'(subject, message) VALUES (\'{request.POST["subject"]}\', '
                f'\'{request.POST["message"]}\');'
            )
            queries = [q for q in query.split(';') if q]
            all_responses = []
            for query in queries:
                try:
                    res = cursor.execute(query)
                    all_responses += res.fetchall()
                except OperationalError:
                    # invalid sql is expected; it will come from the remnants
                    # after the escaped sql.
                    logger.debug(f'Invalid sql: {query}')
    return render(request, 'sql_vulnerable/formpage.html')
