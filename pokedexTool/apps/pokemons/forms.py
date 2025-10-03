from django import forms


class PokemonSearchForm(forms.Form):
    pokemon_name = forms.CharField(
        label='Pokemon name',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'border rounded-lg px-3 py-2 w-full',
            'placeholder': 'Enter Pokemon Name or ID'
        })
    )
