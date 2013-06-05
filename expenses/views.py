from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from expenses.models import *
from django.core.urlresolvers import reverse_lazy
from expenses.forms import *
from auth.views import LoginRequiredViewMixin

class ExpenseList(LoginRequiredViewMixin, ListView):
    model = Expense

    def get_context_data(self, **kwargs):
        context = super(ExpenseList, self).get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context

class ExpenseCreate(LoginRequiredViewMixin, CreateView):
    model = Expense
    success_url = reverse_lazy('expense_list')

class ExpenseUpdate(LoginRequiredViewMixin, UpdateView):
    model = Expense
    success_url = reverse_lazy('expense_list')

class ExpenseDelete(LoginRequiredViewMixin, DeleteView):
    model = Expense
    success_url = reverse_lazy('expense_list')

class RefundCreate(LoginRequiredViewMixin, CreateView):
    model = Refund
    form_class = RefundForm
    success_url = reverse_lazy('expense_list')

class RefundDelete(LoginRequiredViewMixin, DeleteView):
    model = Refund
    success_url = reverse_lazy('expense_list')