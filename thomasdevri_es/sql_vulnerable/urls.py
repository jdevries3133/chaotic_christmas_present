from django.urls import path

from .views import (
    index,
    formpage,
)

urlpatterns = [
    path('', index, name='index'),
    path('contact/', formpage, name='formpage'),
]
