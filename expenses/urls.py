from django.conf.urls import patterns, url

from expenses.views import *

urlpatterns = patterns('',
	url(r'^$', ExpenseList.as_view(), name='expense_list'),
	url(r'^add/$', ExpenseCreate.as_view(), name='expense_create'),
	url(r'^(?P<pk>\d+)/edit/$', ExpenseUpdate.as_view(), name='expense_update'),
	url(r'^(?P<pk>\d+)/delete/$', ExpenseDelete.as_view(), name='expense_delete'),
)