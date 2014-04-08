from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User as DjangoUser
from django.db.models import Sum, Count
from django.core.urlresolvers import reverse
import hashlib
from time import mktime
from datetime import date
from decimal import Decimal


class GroupManager(models.Manager):
    """
    Augments the User model in django.contrib.auth with additional functionality:
    
    When retrieving  the queryset, the manager automatically: 

    - Applies select_related on the User model so its expenses are selected
    - Calculates the sum of the user's expenses and puts it in expense_total
    """

    def get_query_set(self):
        return super(GroupManager, self).get_query_set().select_related('expenses','users').annotate(user_count=Count('users'))


class Group(models.Model):
    """
    Works in a similar fashion to the default Django groups, but without unique names, and with a creation date
    """
    name = models.CharField(_('Group name'), max_length=80, unique=False)
    date_created = models.DateTimeField(_('Creation date'), auto_now_add=True)

    users = models.ManyToManyField(DjangoUser, related_name='expense_groups')  # We must use the DjangoUser becaus proxies cannot see expense_groups
    users_can_edit = models.BooleanField(_("Members can edit each other's expenses"), default=True)

    objects = GroupManager()

    def __unicode__(self):
        return self.name

    @property
    def invite_code(self):
        timestamp = int(mktime(self.date_created.timetuple())*1000)
        digest = hashlib.sha1( str(timestamp) + str(self.pk) ).hexdigest()
        return str(digest)[2:12]

    @property
    def invite_url(self):
        return reverse('invite_detail', kwargs={'pk': self.pk, 'hash': self.invite_code})

    def users_with_totals(self, current_user=None):
        user_list = []
        users = self.users.prefetch_related('expenses').all()
        current_user_total = None
        for user in users:
            expenses = user.expenses.all().filter(group=self.pk).aggregate(total=Sum('amount'))
            user_dict = {
                'user': user,
                'total': expenses['total'] or Decimal('0')
            }

            #If we loop over the current user, add his total
            if current_user and current_user.pk == user.pk:
                current_user_total = expenses['total']

            user_list.append(user_dict)


        #Set the relative totals
        if current_user_total:
            for user_dict in user_list:
                user_dict['relative_total'] = user_dict['total'] - current_user_total

        return user_list

    def get_absolute_url(self):
        return reverse('expense_list', kwargs={'group':self.pk})

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')


class Expense(models.Model):
    """
    A basic expense. Each expense is made by one user, and is added to the user's total expenses
    """
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    description = models.TextField(verbose_name=_('Description'), blank=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Amount'))
    date = models.DateField(default=date.today, verbose_name=_('Date'))
    user = models.ForeignKey(DjangoUser, verbose_name=_('Buyer'), related_name='expenses')
    group = models.ForeignKey(Group, verbose_name=_('Group'))
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['-date','pk']
        get_latest_by = 'date'
        verbose_name = _('Expense')
        verbose_name_plural = _('Expenses')


class Refund(models.Model):
    """
    A basic expense. Each expense is made by one user, and is added to the user's total expenses
    """
    expense_from = models.OneToOneField(Expense, verbose_name=_('From'), related_name='refund_from')
    expense_to = models.OneToOneField(Expense, verbose_name=_('To'), related_name='refund_to')

    description = models.TextField(verbose_name=_('Notes'), blank=True)

    def __unicode__(self):
        return _("Refund to %s") % self.expense_to.user.get_full_name()

    def delete(self, *args, **kwargs):
        self.expense_from.delete()
        self.expense_to.delete()
        return super(Refund, self).delete(*args, **kwargs)
        
    class Meta:
        verbose_name = _('Refund')
        verbose_name_plural = _('Refunds')