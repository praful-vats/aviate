# from rest_framework.decorators import api_view
# from candidates.models import Candidate
# from django.shortcuts import render
# from django.core.paginator import Paginator
# from django.db.models import Q

# @api_view(['GET'])
# def search_candidates(request):
#     candidates = Candidate.objects.all()

#     expected_salary_min = request.GET.get('expected_salary_min')
#     expected_salary_max = request.GET.get('expected_salary_max')
#     age_min = request.GET.get('age_min')
#     age_max = request.GET.get('age_max')
#     years_of_exp_min = request.GET.get('years_of_exp_min')
#     phone_number = request.GET.get('phone_number')
#     email = request.GET.get('email')
#     name = request.GET.get('name')
#     search = request.GET.get('search')

#     if expected_salary_min and expected_salary_max:
#         try:
#             expected_salary_min = float(expected_salary_min)
#             expected_salary_max = float(expected_salary_max)
#             candidates = candidates.filter(expected_salary__gte=expected_salary_min, expected_salary__lte=expected_salary_max)
#         except ValueError:
#             pass  

#     if age_min and age_max:
#         try:
#             age_min = int(age_min)
#             age_max = int(age_max)
#             candidates = candidates.filter(age__gte=age_min, age__lte=age_max)
#         except ValueError:
#             pass 

#     if years_of_exp_min:
#         try:
#             years_of_exp_min = int(years_of_exp_min)
#             candidates = candidates.filter(years_of_exp__gte=years_of_exp_min)
#         except ValueError:
#             pass 

#     if phone_number:
#         candidates = candidates.filter(phone_number=phone_number)

#     if email:
#         candidates = candidates.filter(email=email)

#     if name:
#         candidates = candidates.filter(name__icontains=name)

#     if search:
#         candidates = candidates.filter(
#             Q(name__icontains=search) |
#             Q(email__icontains=search) |
#             Q(phone_number__icontains=search)
#         )
    
#     paginator = Paginator(candidates, 10) 
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'candidates/candidate_list.html', {'page_obj': page_obj})


from rest_framework.decorators import api_view
from candidates.models import Candidate
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from candidates.filters import CandidateFilter

@api_view(['GET'])
def search_candidates(request):
    candidates = Candidate.objects.all()
    name = request.GET.get('name')
    search = request.GET.get('search')

    query = name or search

    if query:
        query_words = set(query.lower().split())

        filtered_candidates = []
        for candidate in candidates:
            candidate_name_words = set(candidate.name.lower().split())
            matching_words = len(query_words.intersection(candidate_name_words))
            filtered_candidates.append((candidate, matching_words))

        filtered_candidates.sort(key=lambda x: (-x[1], len(x[0].name)))
        filtered_candidates = [(candidate, count) for candidate, count in filtered_candidates if count > 0]
        candidates = [candidate for candidate, _ in filtered_candidates]

    else:
        candidate_filter = CandidateFilter(request.GET, queryset=candidates)
        candidates = candidate_filter.qs

    paginator = Paginator(candidates, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'candidates/candidate_list.html', {'page_obj': page_obj})