from django.urls import path
from .views import name_based_search

urlpatterns = [
    path('name-search/', name_based_search, name='name-based-search'),
]
