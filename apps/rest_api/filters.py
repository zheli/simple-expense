import django_filters
from apps.core.models import Expense

class ExpenseFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(name='date', lookup_type='gte')
    end_date = django_filters.DateFilter(name='date', lookup_type='lte')

    class Meta:
        model = Expense
        fields = ['start_date', 'end_date']
