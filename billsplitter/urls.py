from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),

	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}),
	url(r'^logout/$', 'django.contrib.auth.views.logout', kwargs={'next_page':'/'}),

	#Apps
	url(r'', include('social_auth.urls')),
	url(r'^', include('expenses.urls')),
)

#Server static files in debug mode
if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {
		'document_root': settings.MEDIA_ROOT}))
	urlpatterns += staticfiles_urlpatterns()