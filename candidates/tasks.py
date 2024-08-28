from celery import shared_task
from .models import Candidate

@shared_task
def process_candidate_data(candidate_id):
    try:
        candidate = Candidate.objects.get(id=candidate_id)
    except Candidate.DoesNotExist:
        pass
