from django.forms.widgets import ClearableFileInput, DateInput, TimeInput
from django.utils.translation import ugettext_lazy

#Standard inputs for images, dates and times


class ImagePreviewInput(ClearableFileInput):
    """
    Provides the file input with a preview for image uploads
    """
    clear_checkbox_label = ugettext_lazy('No picture')
    template_with_initial = '%(initial)s<br/>%(clear_template)s%(input)s'
    template_with_clear = '<label>%(clear)s %(clear_checkbox_label)s</label>'
    url_markup_template = '<a href="{0}"><img class="img-polaroid" width="150" src="{0}" alt="" />{1}</a>'


class DatePickerInput(DateInput):
    """
    Adds the 'datepicker' class to the input
    """
    def render(self, name, value, attrs=None):
        attrs['type'] = 'date'
        attrs['class'] = 'datepicker'
        attrs['placeholder'] = ugettext_lazy('Select a date')
        return super(DatePickerInput, self).render(name, value, attrs)


class TimePickerInput(TimeInput):
    """
    Adds the 'timepicker' class to the input
    """
    def render(self, name, value, attrs=None):
        attrs['type'] = 'time'
        attrs['class'] = 'timepicker'
        attrs['placeholder'] = ugettext_lazy('...')
        return super(TimePickerInput, self).render(name, value, attrs)
