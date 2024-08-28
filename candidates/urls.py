from django.urls import path
from .views import CandidateListCreateView, CandidateDetailView, search_candidates, candidate_list_view, shortlist_candidate, reject_candidate, search_form, CandidateListView, create_candidate, PaginatedCandidateListView

urlpatterns = [
    path('', CandidateListCreateView.as_view(), name='candidate-list-create'),
    path('<int:pk>/', CandidateDetailView.as_view(), name='candidate-detail'),
    # path('search/', CandidateSearchView.as_view(), name='candidate-search'),
    # path('list/', candidate_list, name='candidate-list'),
    # path('list/', candidate_list_view, name='candidate-list'),
    path('search/', search_candidates, name='search-candidates'),
    # path('search-form/', search_form, name='search-form'),
    path('<int:pk>/shortlist/', shortlist_candidate, name='shortlist-candidate'),
    path('<int:pk>/reject/', reject_candidate, name='reject-candidate'),
    # path('candidates/', CandidateListView.as_view(), name='candidate-list'),
    # path('candidates/', PaginatedCandidateListView.as_view(), name='candidate-list'),
    path('candidates/<int:pk>/', CandidateDetailView.as_view(), name='candidate-detail'),
    path('create/', create_candidate, name='create-candidate'),
]
