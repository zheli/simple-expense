from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework import permissions, serializers
from apps.core.models import Expense, WeekNumber

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
        write_only_fields = ('password', )

    def restore_object(self, attrs, instance=None):
        # encrypt user password
        user = super(UserSerializer, self).restore_object(attrs, instance)
        user.set_password(attrs['password'])
        return user

class WeekNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeekNumber
        fields = ('year', 'number',)

class WeekNumberStatSerializer(WeekNumberSerializer):
#    year_week_number = serializers.SerializerMethodField('get_year_week_number')
    total_spending = serializers.DecimalField()
    average_day_spending = serializers.SerializerMethodField('get_average_day_spending')
    week_number = serializers.IntegerField(source='number')

    class Meta:
        model = WeekNumber
#        fields = ('year', 'week_number','year_week_number', 'total_spending', 'average_day_spending')
        fields = ('year', 'week_number', 'total_spending', 'average_day_spending')

    def get_average_day_spending(self, obj):
        return Decimal(obj.total_spending/7).quantize(Decimal('.01'))

class ExpenseSerializer(serializers.ModelSerializer):
    date = serializers.DateField(required=False)
    time = serializers.TimeField(required=False)
    week_number = serializers.Field(source='week_number.number')

    class Meta:
        model = Expense
        fields = ('id', 'date', 'time', 'amount', 'description', 'comment', 'week_number', 'datetime')
        read_only_fields = ('datetime', )
