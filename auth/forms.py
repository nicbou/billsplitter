from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class UserForm(forms.ModelForm):
	"""
	A limited user form
	"""
	class Meta:
		model = User
		fields = ['first_name','last_name','email']