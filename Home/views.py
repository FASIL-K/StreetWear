from django.shortcuts import render
from category.models import *
from products.models import *

# Create your views here.
def home(request):
    return render(request,'user\home\home.html')

