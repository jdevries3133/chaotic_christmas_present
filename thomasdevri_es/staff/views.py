from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

from .validators import MarkdownSlugPathValidator

# Create your views here.
def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'),
            )
            if user:
                login(request, user)
                return redirect('dashboard')
    return render(request, 'staff/login.html', {'form': AuthenticationForm()})

def dashboard(request):
    return render(request, 'staff/dashboard.html')

def documentation(request, markdownslug):
    slugval = MarkdownSlugPathValidator(markdownslug)
    if not slugval.is_valid():
        return render(request, 'staff/docs/not_found.html', {"bad_slug": markdownslug})
