from django.urls import path

from .views import (
    login_view,
    dashboard,
)

urlpatterns = [
    path('login/', login_view, name='staff_login'),
    path('dashboard/', dashboard, name='dashboard'),
]
