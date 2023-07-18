from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField(max_length=1000,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=50,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.name

