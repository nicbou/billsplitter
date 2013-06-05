from django.conf.urls import patterns, url

from auth.views import *

urlpatterns = patterns('',
	url(r'^account/$', UserUpdate.as_view(), name='user_update'),
)