from django.shortcuts import render, redirect
from .models import Candidate
from rest_framework import generics
from .serializers import CandidateSerializer
from .tasks import process_candidate_data
from django.contrib import messages
from .forms import CandidateForm
import logging
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def typeform_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        form_responses = data.get('form_response', {}).get('answers', [])
        
        candidate_data = {}
        for response in form_responses:
            field_id = response.get('field', {}).get('id')
            answer = response.get('text') or response.get('number')

            if field_id == 'your_field_id_for_name':
                candidate_data['name'] = answer
            elif field_id == 'your_field_id_for_age':
                candidate_data['age'] = answer
            elif field_id == 'your_field_id_for_gender':
                candidate_data['gender'] = answer
            elif field_id == 'your_field_id_for_years_of_exp':
                candidate_data['years_of_experience'] = answer
            elif field_id == 'your_field_id_for_phone_number':
                candidate_data['phone_number'] = answer
            elif field_id == 'your_field_id_for_email':
                candidate_data['email'] = answer
            elif field_id == 'your_field_id_for_current_salary':
                candidate_data['current_salary'] = answer
            elif field_id == 'your_field_id_for_expected_salary':
                candidate_data['expected_salary'] = answer

        Candidate.objects.create(**candidate_data)

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'invalid request'}, status=400)