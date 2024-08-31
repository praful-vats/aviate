import django_filters
from .models import Candidate

class CandidateFilter(django_filters.FilterSet):
    expected_salary = django_filters.NumericRangeFilter(field_name='expected_salary', lookup_expr='range')
    age = django_filters.NumericRangeFilter(field_name='age', lookup_expr='range')
    years_of_exp = django_filters.NumberFilter(field_name='years_of_exp', lookup_expr='gte')
    phone_number = django_filters.CharFilter(field_name='phone_number', lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Candidate
        fields = ['expected_salary', 'age', 'years_of_exp', 'phone_number', 'email', 'name']
        order_by = None
