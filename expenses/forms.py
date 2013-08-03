from django import forms
from expenses.models import Group, Expense, Refund
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from betterforms.widgets import DatePickerInput

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'users_can_edit']

class UserModelChoiceField(forms.ModelChoiceField):
    # Normally, we would simply use the proxy model from expenses.models
    # See expenses.models.Group for more details
    def label_from_instance(self, user):
        return user.get_full_name()

class ExpenseForm(forms.ModelForm):
    user = UserModelChoiceField(label=_("From"),queryset=User.objects.all(), empty_label=_("Select a person"))

    def __init__(self, *args, **kwargs):
        users = kwargs.pop('users', None)
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget = DatePickerInput()

        if users:
            self.fields['user'].queryset = users

    class Meta:
        model = Expense
        exclude = ['group']


class RefundForm(forms.ModelForm):
    """
    Adds improved photo and date widgets to the form, as well as validation
    """
    from_user = UserModelChoiceField(label=_("From"),queryset=User.objects.all(), empty_label=_("Select a person"))
    to_user = UserModelChoiceField(label=_("To"),queryset=User.objects.all(), empty_label=_("Select a person"))
    amount = forms.DecimalField(min_value=0, max_digits=7, decimal_places=2)


    def __init__(self, *args, **kwargs):
        users = kwargs.pop('users', None)
        super(RefundForm, self).__init__(*args, **kwargs)

        if users:
            self.fields['from_user'].queryset = users
            self.fields['to_user'].queryset = users

    def clean(self):
        cleaned_data = super(RefundForm, self).clean()
        if cleaned_data.get("from_user") == cleaned_data.get("to_user"):
            raise ValidationError(_("The refund must be made between two different people"))
        return cleaned_data

    class Meta:
        model = Refund
        fields = ['from_user','to_user','amount','description']