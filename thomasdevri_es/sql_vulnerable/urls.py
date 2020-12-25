from django.urls import path

from .views import (
    index,
    formpage,
    robots,
)

urlpatterns = [
    path('', index, name='index'),
    path('contact/', formpage, name='formpage'),
    path('robots.txt', robots, name='robots'),
]
