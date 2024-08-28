from django.urls import path
from .views import search_candidates

urlpatterns = [
    path('search/', search_candidates, name='search-candidates'),
]
