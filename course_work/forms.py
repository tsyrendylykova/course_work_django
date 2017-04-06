from django import forms
from .models import Driver

class IndexForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ('login', 'password',)
