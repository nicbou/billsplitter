from django import forms
from expenses.models import *
from django.utils.translation import ugettext_lazy as _

class GroupForm(forms.ModelForm):
	class Meta:
		model = Group
		fields = ['name']

class ExpenseForm(forms.ModelForm):
	class Meta:
		model = Expense
		exclude = ['group']

class RefundForm(forms.ModelForm):
	"""
	Adds improved photo and date widgets to the form, as well as validation
	"""
	from_user = forms.ModelChoiceField(label=_("From"),queryset=User.objects.all(), empty_label=_("Select a person"))
	to_user = forms.ModelChoiceField(label=_("To"),queryset=User.objects.all(), empty_label=_("Select a person"))
	amount = forms.IntegerField(min_value=0)

	def clean(self):
		cleaned_data = super(RefundForm, self).clean()
		if cleaned_data.get("from_user") == cleaned_data.get("to_user"):
			raise ValidationError(_("The refund must be made between two different people"))
		return cleaned_data

	class Meta:
		model = Refund
		fields = ['from_user','to_user','amount','description']