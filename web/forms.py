from functools import partial
from django import forms

StartDate = partial(forms.DateInput, {'class': 'start_date'})
EndDate = partial(forms.DateInput, {'class': 'end_date'})

class LocationForm(forms.Form):
    location = forms.CharField(label='Location', max_length=100)

class DateFromForm(forms.Form):
    date_from = forms.DateField(widget=StartDate())
    
class DateToForm(forms.Form):
    date_to = forms.DateField(widget=EndDate())