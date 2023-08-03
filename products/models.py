from django.db import models
from category.models import Brand,Category
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class price_range(models.Model):
    low = models.IntegerField()
    high = models.IntegerField()


class Size(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
# product
class Product(models.Model):
    image1 = models.ImageField(upload_to='media/products',default="no images")
    image2 = models.ImageField(upload_to='media/products',default="no images")
    image3 = models.ImageField(upload_to='media/products',default="no images")
    product_name = models.CharField(unique=True,max_length=50)
    product_price = models.IntegerField()
    sizes = models.ManyToManyField(Size)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    product_description = models.TextField(blank=True)
    is_available = models.BooleanField(default=False)
    slug = models.SlugField(max_length=250,unique=True)
    

    def save(self, *args, **kwargs):
        # generate slug field from name field if slug is empty
        if not self.slug:
            self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)
    def __str__(self):
        return self.product_name
    
    