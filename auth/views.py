from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class LoginRequiredView(object):
	"""
	Replaces the login_required() decorator of function-based views
	"""
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(LoginRequiredView, self).dispatch(*args, **kwargs)