from django.db import models
from django.contrib.auth.models import User
from .import forms

# Create your models here.
class UserModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True,related_name='user')
    balance = models.DecimalField(default=0,max_digits=12,decimal_places=2)
    def __str__(self):
        return self.user.username