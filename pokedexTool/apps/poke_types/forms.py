from django import forms


class TypeSearchForm(forms.Form):
    poke_type_name_or_id = forms.CharField(
        label="Type name or ID",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "border rounded-lg px-3 py-2 w-full",
                "placeholder": "Enter type name or ID",
            }
        ),
    )
