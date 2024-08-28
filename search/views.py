from rest_framework.decorators import api_view
from rest_framework.response import Response
from candidates.models import Candidate
from candidates.serializers import CandidateSerializer
from rest_framework import status
from django.shortcuts import render

@api_view(['GET'])
def name_based_search(request):
    query = request.GET.get('q', '').lower()
    if not query:
        return render(request, 'candidates/candidate_list.html', {'candidates': []})

    exact_matches = Candidate.objects.filter(name__iexact=query)
    partial_matches = Candidate.objects.filter(name__icontains=query).exclude(id__in=exact_matches.values_list('id', flat=True))

    def relevance(candidate):
        name_parts = candidate.name.lower().split()
        query_parts = query.split()
        overlapping_words = len(set(name_parts) & set(query_parts))
        return overlapping_words

    partial_matches = sorted(partial_matches, key=relevance, reverse=True)

    candidates = list(exact_matches) + partial_matches
    return render(request, 'candidates/candidate_list.html', {'candidates': candidates})
