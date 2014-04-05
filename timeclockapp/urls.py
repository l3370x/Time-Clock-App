from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'timeclockapp.views.home', name='home'),
    url(r'^login/', 'timeclockapp.views.home', name='login'),
    url(r'^home/', 'timeclockapp.views.user_view', name='emphome'),
    url(r'^clockin/', 'timeclockapp.views.clockin', name='clockin'),
    url(r'^clockout/', 'timeclockapp.views.clockout', name='clockout'),
    url(r'^new/', 'timeclockapp.views.create', name='create'),
    url(r'^forgot/', 'timeclockapp.views.forgot', name='forgot'),
    url(r'^admin/', include(admin.site.urls)),
)
