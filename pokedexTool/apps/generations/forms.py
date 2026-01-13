from django import forms


class GenerationSearchForm(forms.Form):
    generation_name_or_id = forms.CharField(
        label="Generation name or ID",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "border rounded-lg px-3 py-2 w-full",
                "placeholder": "Enter name or ID",
            }
        ),
    )
