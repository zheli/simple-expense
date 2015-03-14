import base64
import logging
from datetime import date, time
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.test import APIRequestFactory, APIClient
from apps.core.models import Expense
from .serializers import UserSerializer

PASSWORD = 'password'

def get_basic_auth(username):
    credentials = ('%s:password' % username)
    base64_credentials = base64.b64encode(credentials.encode(HTTP_HEADER_ENCODING)).decode(HTTP_HEADER_ENCODING)
    return 'Basic %s' % base64_credentials

# Create your tests here.
class BaseTestCase(TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        self.main_user = User.objects.create_user(
            username='tester1',
            first_name = "tester1",
            last_name = "tester1",
            email='tester1@test.com',
            password=PASSWORD
        )
        self.client = APIClient()
        self.first_expense = Expense(
                user=self.main_user,
                date=date(2014,07,01),
                time=time(8,0,0),
                amount=100,
                description="this is a test description",
                comment="this is a test comment"
        )
        self.first_expense.save()
        self.secondary_user = User.objects.create_user(username='tester2', first_name = "tester2", last_name = "tester2",
            email='tester2@test.com', password=PASSWORD)
        self.e_2013_w_1_1, _ = Expense.objects.get_or_create(user=self.main_user, date=date(2013,01,02),
                time=time(8,0,0), amount=1, description="this is a test description", comment="this is a test comment")
        self.e_2013_w_1_2, _ = Expense.objects.get_or_create(user=self.main_user, date=date(2013,01,05),
                time=time(8,0,0), amount=10, description="this is a test description", comment="this is a test comment")
        self.e_2014_w_1_1, _ = Expense.objects.get_or_create(user=self.main_user, date=date(2014,01,05),
                time=time(8,0,0), amount=2, description="this is a test description", comment="this is a test comment")
        self.e_2014_w_1_2, _ = Expense.objects.get_or_create(user=self.main_user, date=date(2014,01,04),
                time=time(8,0,0), amount=20, description="this is a test description", comment="this is a test comment")
        self.e_2014_w_1_3, _ = Expense.objects.get_or_create(user=self.secondary_user, date=date(2014,01,05),
                time=time(8,0,0), amount=200, description="this is a test description", comment="this is a test comment")

class UserAuthTest(BaseTestCase):
    def test_correct_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION=get_basic_auth(self.main_user))
        url = reverse("authenticate")
        self.logger.debug('Send post request to [{}]'.format(url))
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, UserSerializer(self.main_user).data)

    def test_incorrect_credentials(self):
        url = reverse("authenticate")
        self.client.credentials(HTTP_AUTHORIZATION=get_basic_auth('not_existing_user'))
        self.logger.debug('Send post request to [{}]'.format(url))
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {u'detail': u'Invalid username/password'})

class ExpenseTest(BaseTestCase):
    def setUp(self):
        super(ExpenseTest,self).setUp()
        self.client.credentials(HTTP_AUTHORIZATION=get_basic_auth(self.main_user))

    def test_filter_expense(self):
        # filter all 2013 expenses
        url = '{}?start_date={}&end_date={}'.format(reverse('expense-list'),'2013-01-01','2013-12-31')
        self.logger.debug('Send put request to [{}]'.format(url))
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)

        # filter all 2014 expenses
        url = '{}?start_date={}&end_date={}'.format(reverse('expense-list'),'2014-01-01','2014-12-31')
        self.logger.debug('Send put request to [{}]'.format(url))
        response = self.client.get(url)
        self.assertEqual(len(response.data), 3)

class StatisticsTest(BaseTestCase):
    def setUp(self):
        super(StatisticsTest,self).setUp()
        self.client.credentials(HTTP_AUTHORIZATION=get_basic_auth(self.main_user))

    def test_get_all_stats(self):
        url = reverse('stats-list')
        self.logger.debug('Send put request to [{}]'.format(url))
        response = self.client.get(url)
        self.assertEqual(len(response.data), 3)

    def test_get_2013_stats(self):
        url = '{}?year={}'.format(reverse('stats-list'), '2013')
        self.logger.debug('Send put request to [{}]'.format(url))
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)

    def test_get_2014_stats(self):
        url = '{}?year={}'.format(reverse('stats-list'), '2014')
        self.logger.debug('Send put request to [{}]'.format(url))
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)

    def test_get_other_user_stats(self):
        self.client.credentials(HTTP_AUTHORIZATION=get_basic_auth(self.secondary_user))
        url = reverse('stats-list')
        self.logger.debug('Send put request to [{}]'.format(url))
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
