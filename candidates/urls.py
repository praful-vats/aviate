from django.urls import path
from .views import search_candidates, shortlist_candidate, reject_candidate, create_candidate, CandidateListCreateView, CandidateDetailView

urlpatterns = [
    path('', CandidateListCreateView.as_view(), name='candidate-list-create'),
    path('<int:pk>/', CandidateDetailView.as_view(), name='candidate-detail'),
    path('search/', search_candidates, name='search-candidates'),
    path('<int:pk>/shortlist/', shortlist_candidate, name='shortlist-candidate'),
    path('<int:pk>/reject/', reject_candidate, name='reject-candidate'),
    path('create/', create_candidate, name='create-candidate'),
]
