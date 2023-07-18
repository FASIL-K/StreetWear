from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserOTP(models.Model):
    time_st=models.DateTimeField(auto_now=True)
    otp=models.IntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
