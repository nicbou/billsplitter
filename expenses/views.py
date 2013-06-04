from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from expenses.models import *
from django.core.urlresolvers import reverse_lazy
from expenses.forms import *
from auth.views import LoginRequiredView

class ExpenseList(LoginRequiredView, ListView):
    model = Expense

    def get_context_data(self, **kwargs):
        context = super(ExpenseList, self).get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context

class ExpenseCreate(LoginRequiredView, CreateView):
    model = Expense
    success_url = reverse_lazy('expense_list')

class ExpenseUpdate(LoginRequiredView, UpdateView):
    model = Expense
    success_url = reverse_lazy('expense_list')

class ExpenseDelete(LoginRequiredView, DeleteView):
    model = Expense
    success_url = reverse_lazy('expense_list')

class RefundCreate(LoginRequiredView, CreateView):
    model = Refund
    form_class = RefundForm
    success_url = reverse_lazy('expense_list')

class RefundDelete(LoginRequiredView, DeleteView):
    model = Refund
    success_url = reverse_lazy('expense_list')