from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render
from django.utils.timezone import now
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.core.models import Expense, WeekNumber
from utils import get_week_days
from .filters import ExpenseFilter
from .serializers import WeekNumberStatSerializer, ExpenseSerializer, UserSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    This is a test!
    """
    model = User
    serializer_class = UserSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    """
    This is a test!
    """
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated,]
    queryset = Expense.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ExpenseFilter

    def get_queryset(self):
        queryset = super(ExpenseViewSet, self).get_queryset()
        return queryset.filter(user=self.request.user)
        print('get_query')
        print(self.request.DATA)
        print(self.request.QUERY_PARAMS)
        print(self.request.method)
        return queryset

    def pre_save(self, obj):
        obj.user = self.request.user
        print('pre_save')
        print(self.request.DATA)
        print(self.request.QUERY_PARAMS)
        print(self.request.method)
        super(ExpenseViewSet, self).pre_save(obj)

class StatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WeekNumberStatSerializer
    permission_classes = [IsAuthenticated,]
    queryset = WeekNumber.objects.all()
    lookup_field = 'week_number'

    def get_queryset(self):
        query_year = self.request.QUERY_PARAMS.get('year')
        queryset = super(StatisticsViewSet, self).get_queryset().filter(expense__user=self.request.user)
        if query_year:
            queryset = queryset.filter(year=query_year)
        return queryset.order_by('year', 'number').annotate(total_spending=Sum('expense__amount'))
