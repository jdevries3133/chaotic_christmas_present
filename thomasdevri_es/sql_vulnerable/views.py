from django.shortcuts import render
from django.db import connection

def index(request):
    return render(request, 'sql_vulnerable/home.html')

def formpage(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            # TODO: should exec something like this normally, like django does:
            # INSERT INTO "sql_vulnerable_contactformdata" ("subject", "message") VALUES (\'foo\', \'bar\')', 'time': '0.003
            res = cursor.execute(request.POST['message'])
            out = []
            for i in res.fetchall():
                out += i
    return render(request, 'sql_vulnerable/formpage.html')
