from django.db import models
from category.models import Category
# Create your models here.
class Banner(models.Model):
    banners_image       = models.ImageField(upload_to='photos/banner')
    banner_name         = models.CharField(max_length=200)
    banner_discription  = models.TextField(max_length=200)
    category            = models.ForeignKey(Category, on_delete=models.CASCADE,default=None)
    def __str__(self):
      return self.banner_name