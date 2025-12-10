from django import forms


class LocationSearchForm(forms.Form):
    location_name_or_id = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "border rounded-lg px-3 py-2 w-full",
                "placeholder": "Example: 'canalave-city' or '1'",
            }
        ),
    )

class AreaSearchForm(forms.Form):
    location_name_or_id = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "border rounded-lg px-3 py-2 w-full",
                "placeholder": "Example: 'canalave-city-area' or '1'",
            }
        ),
    )
