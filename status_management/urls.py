from django.urls import path
from .views import CandidateStatusUpdateView, shortlist_candidate, reject_candidate

urlpatterns = [
    path('<int:pk>/', CandidateStatusUpdateView.as_view(), name='candidate-status-update'),
    path('<int:pk>/shortlist/', shortlist_candidate, name='shortlist-candidate'),
    path('<int:pk>/reject/', reject_candidate, name='reject-candidate'),
]
