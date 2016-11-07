from django import forms


class DepartureForm(forms.Form):
    vehicle = forms.CharField(label='Vehicle', max_length=20)
    user = forms.CharField(label='Username', max_length=50)
    odometer = forms.IntegerField(min_value=0, max_value=500000)
