from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from apps.core.models import Expense
from utils import randomDate
import random

class Command(BaseCommand):
    help = 'Create data example for testing'

    def handle(self, *args, **kwargs):
        for i in range(0, 99):
            new_date = randomDate("2013-1-1T0:00", "2013-12-31T23:59", random.random())
            new_amount = random.randint(0, 1000)
            tester1 = User.objects.filter(pk=2)[0]
            Expense.objects.get_or_create(
                    user = tester1,
                    date = new_date.date(),
                    time = new_date.time(),
                    description = "This is a test expense of {}".format(new_amount),
                    comment = "This expense is reported on {}".format(new_date.isoformat()),
                    amount = new_amount
                    )

        for i in range(0, 99):
            new_date = randomDate("2014-1-1T0:00", "2014-12-31T23:59", random.random())
            new_amount = random.randint(0, 1000)
            tester1 = User.objects.filter(pk=2)[0]
            Expense.objects.get_or_create(
                    user = tester1,
                    date = new_date.date(),
                    time = new_date.time(),
                    description = "This is a test expense of {}".format(new_amount),
                    comment = "This expense is reported on {}".format(new_date.isoformat()),
                    amount = new_amount
                    )
        self.stdout.write('Created 200 new expenses!')
