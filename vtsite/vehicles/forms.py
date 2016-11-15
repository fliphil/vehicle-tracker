from django import forms


class DepartureForm(forms.Form):
    vehicle = forms.ChoiceField(label='Vehicle', choices=[(x, x) for x in range(1, 11)])
    user = forms.CharField(label='Username', max_length=50, required=True)
    destination = forms.CharField(label='Destination', max_length=50, required=True)
    odometer = forms.IntegerField(min_value=0, max_value=500000, required=True)
    isFuelFull = forms.BooleanField(label='Fuel Tank Filled', required=True)
    wereTiresInspected = forms.BooleanField(label='Tires Inspected', required=True)
    completedDamageInspection = forms.BooleanField(label='Checked for damage to vehicle', required=True)

class ArrivalForm(forms.Form):
    # can we prepopulate this field with the vehicle they checked out...?
    vehicle = forms.ChoiceField(label='Vehicle', choices=[(x, x) for x in range(1, 11)])
    user = forms.CharField(label='Username', max_length=50, required=True)
    destination = forms.CharField(label='Destination', max_length=50, required=True)
    odometer = forms.IntegerField(min_value=0, max_value=500000, required=True)
    isFuelFull = forms.BooleanField(label='Fuel Tank Filled', required=True)
    trash = forms.BooleanField(label='Is the vehicle free of trash?', required=True)
    damageOrMechanicalProblems = forms.BooleanField(label='Reporting damage or mechanical problems', required=True)
    comments = forms.CharField(label='Comments', max_length=500, required=False)
