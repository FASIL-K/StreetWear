from django.shortcuts import render,redirect
from account.models import User
from django.contrib import messages



# Create your views here.

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('')
    return render(request,'adminside/dashboard.html')

#---------------------------User management -----------------------------

def user_mangement(request):
    users = User.objects.all().order_by('id')
    return render(request,'adminside/usermangement/user_management.html',{'users':users})

def user_block(request,user_id):
    users = User.objects.get(id=user_id)
    if users.is_superuser:
        messages.error(request,"Cannot block superuser")
        return redirect(user_mangement)
    if users.is_blocked is True:
        users.is_blocked =False
        messages.success(request,"Un blocked successfully")
    else:
        users.is_blocked = True
        messages.success(request,"Blocked Successfully")
    users.save()
    return redirect(user_mangement)
    
