from django import forms
from .models import OutletModel

class NotificationRequestForm(forms.Form):
    email_address = forms.EmailField(label='Email Address', max_length=100)
    #mobile_number = forms.CharField(label='Mobile Number (optional)', max_length=20, required=False)
    model = forms.ModelChoiceField(label='Device/Model', queryset=OutletModel.objects.all())
