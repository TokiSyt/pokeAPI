from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username",)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for fieldname in self.fields:
            self.fields[fieldname].help_text = ""
        
class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username",)