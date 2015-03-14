from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from utils import get_week_days

# Create your models here.
class WeekNumber(models.Model):
    year = models.IntegerField()
    number = models.IntegerField()

class Expense(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField()
    time = models.TimeField()
    datetime = models.DateTimeField()
    description = models.CharField(max_length=200)
    amount= models.DecimalField(max_digits=18, decimal_places=2, default=0)
    comment = models.TextField('comment', max_length=1000)
    week_number = models.ForeignKey(WeekNumber)
    #week_number = models.IntegerField('the week number of the year')

    def save(self, *args, **kwargs):
        import datetime
        week_number, created = WeekNumber.objects.get_or_create(year=self.date.year, number=self.date.isocalendar()[1])
        self.datetime = datetime.datetime.combine(date=self.date, time=self.time).replace(tzinfo=timezone.get_current_timezone())
        self.week_number = week_number
        super(Expense, self).save(*args, **kwargs)
