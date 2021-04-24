from django import forms
from .models import request_detail


class DateInput(forms.DateInput):
    input_type = 'date'


class RequestPeriodForm(forms.ModelForm):
    class Meta:
        model = request_detail
        fields = ['return_date']
        widgets = {
            'return_date': DateInput(),
        }
        help_texts = {
            'return_date': 'Enter the date by which you will return the book (Max-3 weeks)',
        }
