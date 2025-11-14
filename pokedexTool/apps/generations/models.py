from django.db import models

class Generation(models.Model):
    
    name = models.CharField(max_length=50, unique=True)
#    gen_id = models.IntegerField()