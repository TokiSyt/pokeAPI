from django.db import models
from django.contrib.auth.models import AbstractUser

'''
from django.contrib.auth import get_user_model
User = get_user_model()
'''

class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username