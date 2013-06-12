from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from auth.forms import *

class LoginRequiredViewMixin(object):
	"""
	Replaces the login_required() decorator of function-based views
	"""
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(LoginRequiredViewMixin, self).dispatch(*args, **kwargs)

class UserUpdate(LoginRequiredViewMixin, UpdateView):
	model = User
	success_url = reverse_lazy('group_list')
	form_class = UserForm

	def get_object(self):
		return self.request.user