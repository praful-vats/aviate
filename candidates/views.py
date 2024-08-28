from django.shortcuts import render, redirect
from .models import Candidate
from rest_framework import status
from rest_framework.decorators import api_view
# Create your views here.
from rest_framework import generics
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Candidate
from .serializers import CandidateSerializer
from django.db.models import Q
from .tasks import process_candidate_data
from django.views.decorators.cache import cache_page
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Candidate
from .serializers import CandidateSerializer
import django_filters
from .filters import CandidateFilter
import logging
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from django.contrib import messages
from .models import Candidate
from .forms import CandidateForm
from .tasks import process_candidate_data

logger = logging.getLogger(__name__)


class CandidateListCreateView(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

class CandidateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

# class CandidateSearchView(APIView):
#     def get(self, request):
#         name = request.query_params.get('name', None)
#         email = request.query_params.get('email', None)
#         phone_number = request.query_params.get('phone_number', None)
#         age_min = request.query_params.get('age_min', None)
#         age_max = request.query_params.get('age_max', None)
#         exp_min = request.query_params.get('exp_min', None)
#         salary_min = request.query_params.get('salary_min', None)
#         salary_max = request.query_params.get('salary_max', None)

#         candidates = Candidate.objects.all()

#         if name:
#             candidates = candidates.filter(name__icontains=name)
#         if email:
#             candidates = candidates.filter(email=email)
#         if phone_number:
#             candidates = candidates.filter(phone_number=phone_number)
#         if age_min and age_max:
#             candidates = candidates.filter(age__gte=age_min, age__lte=age_max)
#         if exp_min:
#             candidates = candidates.filter(years_of_exp__gte=exp_min)
#         if salary_min and salary_max:
#             candidates = candidates.filter(expected_salary__gte=salary_min, expected_salary__lte=salary_max)

#         serializer = CandidateSerializer(candidates, many=True)
#         return Response(serializer.data)

@api_view(['GET'])
def search_candidates(request):
    candidates = Candidate.objects.all()

    expected_salary_min = request.GET.get('expected_salary_min')
    expected_salary_max = request.GET.get('expected_salary_max')
    age_min = request.GET.get('age_min')
    age_max = request.GET.get('age_max')
    years_of_exp_min = request.GET.get('years_of_exp_min')
    phone_number = request.GET.get('phone_number')
    email = request.GET.get('email')
    name = request.GET.get('name')
    search = request.GET.get('search')

    logger.debug(f'Search parameters: {request.GET}')

    if expected_salary_min:
        candidates = candidates.filter(expected_salary__gte=expected_salary_min)
        logger.debug(f'Filtered by expected_salary__gte={expected_salary_min}')
    if expected_salary_max:
        candidates = candidates.filter(expected_salary__lte=expected_salary_max)
        logger.debug(f'Filtered by expected_salary__lte={expected_salary_max}')
    # if age_min:
    #     candidates = candidates.filter(age__gte=age_min)
    #     logger.debug(f'Filtered by age__gte={age_min}')
    # if age_max:
    #     candidates = candidates.filter(age__lte=age_max)
    #     logger.debug(f'Filtered by age__lte={age_max}')
    if age_min and age_max:
        candidates = candidates.filter(age__gte=age_min, age__lte=age_max)
    if years_of_exp_min:
        candidates = candidates.filter(years_of_exp__gte=years_of_exp_min)
        logger.debug(f'Filtered by years_of_exp__gte={years_of_exp_min}')
    if phone_number:
        candidates = candidates.filter(phone_number=phone_number)
        logger.debug(f'Filtered by phone_number={phone_number}')
    if email:
        candidates = candidates.filter(email=email)
        logger.debug(f'Filtered by email={email}')
    if name:
        candidates = candidates.filter(name__icontains=name)
        logger.debug(f'Filtered by name__icontains={name}')
    if search:
        candidates = candidates.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone_number__icontains=search)
        )
        logger.debug(f'Filtered by search={search}')

    print(f"Received Params: age_min={age_min}, age_max={age_max}")
    print(f"Filtered Candidates: {candidates}")

    return render(request, 'candidates/candidate_list.html', {'candidates': candidates})

# def candidate_list_view(request):
#     candidates = Candidate.objects.all()
#     return render(request, 'candidates/candidate_list.html', {'candidates': candidates})

# @cache_page(60 * 15) 
# def candidate_list_view(request):
#     candidates = Candidate.objects.all()
#     return render(request, 'candidates/candidate_list.html', {'candidates': candidates})

@cache_page(60 * 15) 
def candidate_list_view(request):
    candidates_list = Candidate.objects.all()
    paginator = Paginator(candidates_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'candidates/candidate_list.html', {'page_obj': page_obj})

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
    

@api_view(['GET'])
def search_candidates(request):
    candidates = Candidate.objects.all()

    expected_salary_min = request.GET.get('expected_salary_min')
    expected_salary_max = request.GET.get('expected_salary_max')
    age_min = request.GET.get('age_min')
    age_max = request.GET.get('age_max')
    years_of_exp_min = request.GET.get('years_of_exp_min')
    phone_number = request.GET.get('phone_number')
    email = request.GET.get('email')
    name = request.GET.get('name')
    search = request.GET.get('search')

    if expected_salary_min and expected_salary_max:
        candidates = candidates.filter(expected_salary__gte=expected_salary_min, expected_salary__lte=expected_salary_max)

    if age_min and age_max:
        candidates = candidates.filter(age__gte=age_min, age__lte=age_max)

    if years_of_exp_min:
        candidates = candidates.filter(years_of_exp__gte=years_of_exp_min)

    if phone_number:
        candidates = candidates.filter(phone_number=phone_number)

    if email:
        candidates = candidates.filter(email=email)

    if name:
        candidates = candidates.filter(name__icontains=name)

    if search:
        candidates = candidates.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone_number__icontains=search)
        )
    paginator = Paginator(candidates, 10)  # Show 10 candidates per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'candidates/candidate_list.html', {'page_obj': page_obj})



def search_form(request):
    return render(request, 'candidates/search_form.html')


# def create_candidate(request):
#     candidate = Candidate.objects.create(...) 
#     process_candidate_data.delay(candidate.id)
#     return redirect('candidate-list')

def create_candidate(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save()
            
            process_candidate_data.delay(candidate.id)
            
            messages.success(request, 'Candidate created successfully and processing has started.')
            # return redirect('candidate-list')
            return redirect('search-candidates')
        else:
            messages.error(request, 'There was an error with the form submission.')
    else:
        form = CandidateForm()
    
    return render(request, 'candidates/create_candidate.html', {'form': form})

class CandidateListView(generics.ListAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CandidateFilter
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset

class PaginatedCandidateListView(generics.ListAPIView):
    serializer_class = CandidateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CandidateFilter
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        queryset = Candidate.objects.all()

        # Apply filters
        expected_salary_min = self.request.GET.get('expected_salary_min')
        expected_salary_max = self.request.GET.get('expected_salary_max')
        age_min = self.request.GET.get('age_min')
        age_max = self.request.GET.get('age_max')
        years_of_exp_min = self.request.GET.get('years_of_exp_min')
        phone_number = self.request.GET.get('phone_number')
        email = self.request.GET.get('email')
        name = self.request.GET.get('name')
        search = self.request.GET.get('search')

        if expected_salary_min and expected_salary_max:
            queryset = queryset.filter(expected_salary__gte=expected_salary_min, expected_salary__lte=expected_salary_max)

        if age_min and age_max:
            queryset = queryset.filter(age__gte=age_min, age__lte=age_max)

        if years_of_exp_min:
            queryset = queryset.filter(years_of_exp__gte=years_of_exp_min)

        if phone_number:
            queryset = queryset.filter(phone_number=phone_number)

        if email:
            queryset = queryset.filter(email=email)

        if name:
            queryset = queryset.filter(name__icontains=name)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone_number__icontains=search)
            )

        return queryset



class CandidateFilter(django_filters.FilterSet):
    expected_salary_min = django_filters.NumberFilter(field_name='expected_salary', lookup_expr='gte')
    expected_salary_max = django_filters.NumberFilter(field_name='expected_salary', lookup_expr='lte')
    age_min = django_filters.NumberFilter(field_name='age', lookup_expr='gte')
    age_max = django_filters.NumberFilter(field_name='age', lookup_expr='lte')
    years_of_exp_min = django_filters.NumberFilter(field_name='years_of_exp', lookup_expr='gte')

    class Meta:
        model = Candidate
        fields = ['expected_salary_min', 'expected_salary_max', 'age_min', 'age_max', 'years_of_exp_min']