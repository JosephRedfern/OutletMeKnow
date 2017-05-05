from django import forms
from .models import OutletModel

class NotificationRequestForm(forms.Form):
    email_address = forms.EmailField(label='Your Email Address', max_length=100)
    mobile_number = forms.CharField(max_length=20, required=False)
    model = forms.ModelChoiceField(queryset=OutletModel.objects.all())