from rest_framework.decorators import api_view
from candidates.models import Candidate
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q, Case, When, Value, IntegerField, BooleanField
from django.db.models.functions import Length

@api_view(['GET'])
def search_candidates(request):
    name = request.GET.get('name')
    search = request.GET.get('search')
    query = name or search

    candidates = Candidate.objects.all()

    if query:
        query_words = query.lower().split()

        candidates = candidates.annotate(
            matching_words_count=sum(
                Case(
                    When(name__icontains=word, then=1),
                    default=0,
                    output_field=IntegerField(),
                )
                for word in query_words
            ),
            all_words_match=Case(
                When(matching_words_count=len(query_words), then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
            name_word_count=Length('name'),
        )

        candidates = candidates.filter(matching_words_count__gt=0).order_by(
            '-all_words_match',
            '-matching_words_count',
            'name_word_count',
            'name',
        )

    paginator = Paginator(candidates, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'candidates/candidate_list.html', {'page_obj': page_obj})
