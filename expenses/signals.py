from django.db.models.signals import post_save
from django.contrib.auth.models import User
from expenses.models import Group
from django.utils.translation import ugettext as _
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_initial_group(sender, instance, signal, created, **kwargs):
    """
    When a user is created, add a default group
    """
    if created == True:
        group = Group(name=_('Personal expenses'))
        group.save()
        group.users.add(instance)
        group.save()