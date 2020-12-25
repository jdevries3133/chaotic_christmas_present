from pathlib import Path

from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
import markdown

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

# @ staff_member_required
def dashboard(request):
    return render(request, 'staff/dashboard.html')

# @ staff_member_required
def documentation(request, markdownslug):
    # BEGIN MONKEY PATCH; FILE NAME TOO LONG
    secret = (  # secret from round 1 challenge
        'dkBiqWBYnpLwYtcRalgjAEQTtPrcCkobBzZDAcuJOPMRDIzIlcQdigzWRnNbdrWLNLxfpwSjOw'
        'RWQcKIcBPyHenwrVXaInIUgCwfaLoAZwCoNpODeHDwmKrUIiPMFPpxBXGOxkEhRppFOwOUjWgf'
        'SnwlFdQQQarKzicxtTWIXrqurdOQUVGDPlDLEfxBcYFRcOlqzuhNfvYFERVuRgkxGXHWYnhzOH'
        'JJAKDtzhPiiFYcLJAtgsmPsXDlfgfyFhiKoBfSotnNPmdqLRYYurOEWpZoprSWXnHpKwtWzYbk'
        'gnBr'
    )
    try:
        markdownbit = markdownslug.split('.')[1]
        if markdownbit == secret:
            with open(Path(settings.BASE_DIR, 'staff', 'markdown', 'round2', 'wohoo.md'), 'r') as mdf:
                markdown_string = mdf.read()
                return render(request, 'staff/docs/markdown_doc.html', {
                    "doc_title": secret,
                    "rendered_markdown": markdown.markdown(markdown_string)
                })
    except IndexError:
        pass
    # END MONKEYPATCH; FILE NAME TOO LONG

    slugval = MarkdownSlugPathValidator(
        markdownslug,
        Path(settings.BASE_DIR, 'staff', 'markdown')
    )
    if not slugval.is_valid():
        return render(request, 'staff/docs/not_found.html', {"bad_slug": markdownslug})
    with open(slugval.get_path(), 'r') as mdf:
        markdown_string = mdf.read()
    return render(request, 'staff/docs/markdown_doc.html', {
        "doc_title": slugval.get_path().stem,
        "rendered_markdown": markdown.markdown(markdown_string)
    })

# @ staff_member_required
def doclist(request):
    docs = []
    for i in Path(settings.BASE_DIR, 'staff', 'markdown').iterdir():
        if i.name[-3:] != '.md' or i.name[0] == '.' or i.name[0] == '~':
            continue
        docs.append(
            (
                i.stem,
                f'/staff/doc/{i.stem}',
            )
        )
    return render(request, 'staff/docs/doclist.html', {'docs': docs})
