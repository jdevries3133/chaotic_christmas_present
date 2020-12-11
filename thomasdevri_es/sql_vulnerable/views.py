from django.shortcuts import render

def index(request):
    if request.METHOD == 'POST':
        breakpoint()
    return render(request, 'sql_vulnerable/home.html')

def formpage(request):
    return render(request, 'sql_vulnerable/formpage.html')
