from django import forms
from .models import Driver, Location

class IndexForm(forms.Form):
    login = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

class DriverForm(forms.Form):
    start_point = forms.ModelChoiceField(queryset=None, label='start point', to_field_name='name')
    end_point = forms.ModelChoiceField(queryset=None, label='end point', to_field_name='name')
    date = forms.DateField(label='date')
    number_of_free_seats = forms.IntegerField(label='number of free seats')

    def __init__(self, *args, **kwargs):
        super(DriverForm, self).__init__(*args, **kwargs)
        location_list = Location.objects.all()
        self.fields['start_point'].queryset = location_list
        self.fields['end_point'].queryset = location_list
