# urls.py

from django.urls import path
from .views import search_user_by_query

urlpatterns = [
    path('search_user/', search_user_by_query, name='search_user_by_query'),
]

