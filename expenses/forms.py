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

	def save(self, force_insert=False, force_update=False, commit=True):
		refund = super(RefundForm, self).save(commit=False)
		from_amount = self.cleaned_data.get("amount")
		to_amount = -from_amount
		if commit:
			expense_from = Expense(user=self.cleaned_data.get("from_user"), amount=from_amount)
			expense_from.save()
			expense_to = Expense(user=self.cleaned_data.get("to_user"), amount=to_amount)
			expense_to.save()

			refund.expense_from = expense_from
			refund.expense_to = expense_to
			refund.save()
		return refund

	class Meta:
		model = Refund
		fields = ['from_user','to_user','amount','description']