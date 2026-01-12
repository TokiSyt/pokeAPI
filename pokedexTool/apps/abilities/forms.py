from django import forms


class AbilitySearchForm(forms.Form):
    poke_ability_name_or_id = forms.CharField(
        label="Ability name or ID",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "border rounded-lg px-3 py-2 w-full",
                "placeholder": "Enter ability name or ID",
            }
        ),
    )
