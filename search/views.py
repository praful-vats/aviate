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






# from rest_framework.decorators import api_view
# from candidates.models import Candidate
# from django.shortcuts import render
# from django.core.paginator import Paginator

# @api_view(['GET'])
# def search_candidates(request):
#     name = request.GET.get('name')
#     search = request.GET.get('search')
#     query = name or search

#     candidates = Candidate.objects.all()

#     if query:
#         query_words = query.lower().split()

#         def calculate_matching_words_count(name):
#             return sum(word in name.lower() for word in query_words)

#         def is_exact_match(name):
#             return name.lower() == query.lower()

#         candidates_with_count = [
#             (candidate, calculate_matching_words_count(candidate.name), is_exact_match(candidate.name))
#             for candidate in candidates
#         ]

#         candidates_with_count = [
#             (candidate, count, exact) for candidate, count, exact in candidates_with_count if count > 0
#         ]

#         candidates_with_count.sort(
#             key=lambda x: (
#                 not x[2],
#                 -x[1],
#                 len(x[0].name),
#                 x[0].name
#             )
#         )

#         sorted_candidates = [candidate for candidate, _, _ in candidates_with_count]

#     else:
#         sorted_candidates = candidates

#     paginator = Paginator(sorted_candidates, 10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'candidates/candidate_list.html', {'page_obj': page_obj})
