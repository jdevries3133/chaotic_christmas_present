from django.shortcuts import render
from django.db import connection

from sql_vulnerable.models import ContactFormData

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
            res = cursor.execute(query)
    return render(request, 'sql_vulnerable/formpage.html')
