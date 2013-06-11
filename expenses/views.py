from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.detail import DetailView
from expenses.models import *
from django.core.urlresolvers import reverse_lazy
from expenses.forms import *
from auth.views import LoginRequiredViewMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404

class GroupList(LoginRequiredViewMixin, ListView):
    model = Group

    def get_queryset(self):
        return self.request.user.expense_groups.all()

class GroupCreate(LoginRequiredViewMixin, CreateView):
    model = Group
    form_class = GroupForm

    def form_valid(self, form):
        self.object = form.save()
        self.object.users.add(self.request.user)
        return super(GroupCreate, self).form_valid(form) 

class GroupUpdate(LoginRequiredViewMixin, UpdateView):
    model = Group
    form_class = GroupForm

class GroupDelete(LoginRequiredViewMixin, DeleteView):
    model = Group
    success_url = reverse_lazy('group_list')

class InviteCreate(LoginRequiredViewMixin, DetailView):
    """
    Shows the URL to invite people to join a group
    """
    template_name = "expenses/invite_create.html"
    model = Group

    def get_queryset(self):
        return self.request.user.expense_groups.all()

class InviteDetail(LoginRequiredViewMixin, DetailView):
    """
    Shows an invitation, provided that you have a valid invite code
    """
    template_name = "expenses/invite_detail.html"
    model = Group

    def get_object(self,queryset=None):
        group = super(InviteDetail, self).get_object()
        if self.kwargs['hash'] == group.invite_code:
            return group
        else:
            raise Http404

class InviteAccept(LoginRequiredViewMixin, RedirectView):
    """
    Accepts an invitation confirmation via POST, verifies the hash first
    """
    template_name = "expenses/invite_accept.html"
    http_method_names = ['post',]

    def post(self, request, *args, **kwargs):
        group = Group.objects.get(pk=self.kwargs['pk'])
        if self.kwargs['hash'] == group.invite_code:
            group.users.add(request.user)
            return redirect(group.get_absolute_url())
        else:
            raise Http404


class ExpenseList(LoginRequiredViewMixin, ListView):
    model = Expense

    def get_queryset(self):
        try:
            return self.request.user.expense_groups.get(pk=self.kwargs['group']).expense_set.all()
        except Group.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        group = self.request.user.expense_groups.get(pk=self.kwargs['group'])
        context = super(ExpenseList, self).get_context_data(**kwargs)
        context['group'] = group
        return context

class ExpenseCreate(LoginRequiredViewMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    success_url = reverse_lazy('expense_list')

    def get_initial(self):
        """
        Sets the initial user and group to the one specified in the URL
        """
        try:
            group = self.request.user.expense_groups.get(pk=self.kwargs['group'])
        except Group.DoesNotExist:
            raise Http404
        else:
            initial = super(ExpenseCreate, self).get_initial()
            initial = initial.copy() # Copy the dictionary so we don't accidentally change a mutable dict
            initial['group'] = group
            initial['user'] = self.request.user
            return initial

class ExpenseUpdate(LoginRequiredViewMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
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