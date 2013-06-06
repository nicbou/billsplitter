from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User as DjangoUser
from django.db.models import Sum
from django.core.urlresolvers import reverse

class UserManager(models.Manager):
    """
    Augments the User model in django.contrib.auth with additional functionality:
    
    When retrieving  the queryset, the manager automatically: 

    - Applies select_related on the User model so its expenses are selected
    - Calculates the sum of the user's expenses and puts it in expense_total
    """

    def get_query_set(self):
        return super(UserManager, self).get_query_set().select_related('expenses').annotate(expenses_total=Sum('expenses__amount'))

class User(DjangoUser):
    """
    Extends the default User model to add a custom manager with augmented functionality
    """
    objects = UserManager()

    def __unicode__(self):
        return self.get_full_name()

    class Meta:
        proxy = True

class GroupManager(models.Manager):
    """
    Augments the User model in django.contrib.auth with additional functionality:
    
    When retrieving  the queryset, the manager automatically: 

    - Applies select_related on the User model so its expenses are selected
    - Calculates the sum of the user's expenses and puts it in expense_total
    """

    def get_query_set(self):
        return super(GroupManager, self).get_query_set().select_related('expense').annotate(expenses_total=Sum('expense__amount'))

class Group(models.Model):
    """
    Works in a similar fashion to the default Django groups, but without unique names
    """
    name = models.CharField(_('name'), max_length=80, unique=False)
    date_created = models.DateTimeField(_('Creation date'), auto_now_add=True)

    users = models.ManyToManyField(DjangoUser, related_name='expense_groups')

    objects = GroupManager()

    def __unicode__(self):
        return self.name

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
    date = models.DateField(auto_now_add=True, verbose_name=_('Date'))
    user = models.ForeignKey(User, verbose_name=_('Buyer'), related_name='expenses')
    group = models.ForeignKey(Group, verbose_name=_('Group'))
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['-date',]
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
        return _("Refund to %s") % self.expense_to.user

    def delete(self, *args, **kwargs):
        self.expense_from.delete()
        self.expense_to.delete()
        return super(Refund, self).delete(*args, **kwargs)
        
    class Meta:
        verbose_name = _('Refund')
        verbose_name_plural = _('Refunds')