import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.db.utils import OperationalError

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
            return render(request, 'sql_vulnerable/formpage.html', {
                'query_responses': all_responses,
                'real_data': {
                    'subject': request.POST['subject'],
                    'message': request.POST['message'],
                },
            })
    return render(request, 'sql_vulnerable/formpage.html')

def robots(request):
    return HttpResponse(
        (
        'User-agent: *\n'
        'Disallow: /staff/login'
        ),
        content_type="text/plain"
    )
