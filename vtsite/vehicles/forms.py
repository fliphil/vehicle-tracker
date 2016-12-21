from django import forms


class TripBeginForm(forms.Form):
    vehicle = forms.ChoiceField(label='Vehicle', choices=[(x, x) for x in range(1, 11)])
    destination = forms.CharField(label='Destination', max_length=50, required=True)
    odometer = forms.IntegerField(min_value=0, max_value=500000, required=True)
    is_fuel_full = forms.BooleanField(label='Fuel Tank Filled', required=True)
    were_tires_inspected = forms.BooleanField(label='Tires Inspected', required=True)
    completed_damage_inspection = forms.BooleanField(label='Checked for vehicle damage', required=True)


class TripFinishForm(forms.Form):
    odometer = forms.IntegerField(min_value=0,
                                  max_value=500000,
                                  required=True)
    is_fuel_full = forms.BooleanField(label='Fuel Tank Filled',
                                      required=True)
    trash = forms.BooleanField(label='Is the vehicle free of trash?',
                               required=True)
    damage_or_mechanical_problems = forms.BooleanField(label='Reporting damage or mechanical problems',
                                                       required=True)
    comments = forms.CharField(label='Comments',
                               widget=forms.Textarea(attrs={'rows':4, 'cols': 27}),
                               max_length=500,
                               required=False)
