from django import forms


class MoveSearchForm(forms.Form):
    poke_move_name_or_id = forms.CharField(
        label="Move name or ID",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "border rounded-lg px-3 py-2 w-full",
                "placeholder": "Enter move name or ID",
            }
        ),
    )
