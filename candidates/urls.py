from django.urls import path
from . import views
from .views import create_candidate, CandidateDetailView

urlpatterns = [
    path('<int:pk>/', CandidateDetailView.as_view(), name='candidate-detail'),
    path('create/', create_candidate, name='create-candidate'),
    path('webhook/', views.typeform_webhook, name='typeform-webhook'),
]
