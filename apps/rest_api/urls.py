from django.conf.urls import patterns, include, url
from apps.rest_api import views, viewsets
from rest_framework import routers

statistics_week_list_view = viewsets.StatisticsViewSet.as_view({'get': 'list'})
statistics_week_detail_view = viewsets.StatisticsViewSet.as_view({'get': 'retrieve'})

router = routers.DefaultRouter()
router.register(r'users', viewsets.UserViewSet)
router.register(r'expenses', viewsets.ExpenseViewSet)
router.register(r'statistics', viewsets.StatisticsViewSet, base_name='stats')

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
#    url(r'^statistics/$', statistics_week_list_view, name='stat-list'),
#    url(r'^statistics/(?P<year>[0-9]+)/(?P<week>[0-9]+)/$', statistics_week_detail_view, name='stat-week-detail'),
    url(r'^auth/$', views.AuthView.as_view(), name='authenticate')
)
