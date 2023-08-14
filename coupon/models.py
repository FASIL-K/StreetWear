from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.


class Coupon(models.Model):
    coupon = models.CharField(max_length=100)
    coupon_code = models.CharField(max_length=50)
    discount = models.IntegerField(

        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    min_price = models.DecimalField(
        max_digits = 8,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10000)]
    )
    valid_from = models.DateField()
    valid_to = models.DateField()
    is_active =models.BooleanField(default=True)

    def __str__(self) :
        return self.coupon
    
class CouponUsage(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE)
    total_price = models.BigIntegerField(default=0)
    used = models.BooleanField(default=False)
    usage_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.coupon .coupon_code}"
    