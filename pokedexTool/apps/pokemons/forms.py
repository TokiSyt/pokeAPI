from django import forms


class PokemonSearchForm(forms.Form):
    pokemon_name_or_id = forms.CharField(
        label='Pokémon name or ID',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'border rounded-lg px-3 py-2 w-full',
            'placeholder': 'Enter pokemon name or ID'
        })
    )
