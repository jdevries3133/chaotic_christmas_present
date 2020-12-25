from django.urls import path

from .views import (
    login_view,
    dashboard,
    doclist,
    documentation,
)

urlpatterns = [
    path('login/', login_view, name='staff_login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('doclist/', doclist, name='doclist'),
    path('doc/<str:markdownslug>/', documentation, name='documentation'),
]
