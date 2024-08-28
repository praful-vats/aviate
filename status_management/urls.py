from django.urls import path
from .views import CandidateStatusUpdateView

urlpatterns = [
    path('<int:pk>/', CandidateStatusUpdateView.as_view(), name='candidate-status-update'),
]
