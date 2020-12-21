from django.urls import path

from .views import (
    login_view,
    dashboard,
    documentation,
)

urlpatterns = [
    path('login/', login_view, name='staff_login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/doc/<str:markdownslug>/', documentation, name='documentation'),
]
