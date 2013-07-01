from django import template
from datetime import date, timedelta
from auth import utils

register = template.Library()

@register.filter(name='abbreviate')
def abbreviate(value):
    """
    Abbreviates a person's name
    """
    return utils.abbreviate(value)