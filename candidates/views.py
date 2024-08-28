from django.shortcuts import render, redirect
from .models import Candidate
from rest_framework import generics
from .serializers import CandidateSerializer
from .tasks import process_candidate_data
from django.contrib import messages
from .forms import CandidateForm
import logging

logger = logging.getLogger(__name__)

class CandidateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

def create_candidate(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save()
            process_candidate_data.delay(candidate.id)
            messages.success(request, 'Candidate created successfully and processing has started.')
            return redirect('search-candidates')
        else:
            messages.error(request, 'There was an error with the form submission.')
    else:
        form = CandidateForm()
    
    return render(request, 'candidates/create_candidate.html', {'form': form})
