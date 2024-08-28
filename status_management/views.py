from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from candidates.models import Candidate
from candidates.serializers import CandidateSerializer
from rest_framework.decorators import api_view

class CandidateStatusUpdateView(APIView):
    def patch(self, request, pk):
        try:
            candidate = Candidate.objects.get(pk=pk)
        except Candidate.DoesNotExist:
            return Response({'error': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)

        status_update = request.data.get('status')
        if status_update not in ['Shortlisted', 'Rejected']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        candidate.status = status_update
        candidate.save()
        serializer = CandidateSerializer(candidate)
        return Response(serializer.data)

@api_view(['POST'])
def shortlist_candidate(request, pk):
    try:
        candidate = Candidate.objects.get(pk=pk)
        candidate.status = 'Shortlisted'
        candidate.save()
        return Response({'status': 'Candidate shortlisted'}, status=status.HTTP_200_OK)
    except Candidate.DoesNotExist:
        return Response({'error': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def reject_candidate(request, pk):
    try:
        candidate = Candidate.objects.get(pk=pk)
        candidate.status = 'Rejected'
        candidate.save()
        return Response({'status': 'Candidate rejected'}, status=status.HTTP_200_OK)
    except Candidate.DoesNotExist:
        return Response({'error': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)
