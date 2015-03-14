from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', TemplateView.as_view(template_name='base.html')),
    url(r'^api/v1/', include('apps.rest_api.urls')),
    url(r'^api/docs/', include('rest_framework_swagger.urls')),
    # url(r'^$', 'expense_track.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # for browsable API login/logout
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
