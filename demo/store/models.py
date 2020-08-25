
from django.utils import timezone
from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    profession = models.CharField(max_length=200)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
