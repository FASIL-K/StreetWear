from django.shortcuts import render,redirect
from account.models import User
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required



# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='admin_login')
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('')
    return render(request,'adminside/dashboard.html')

#---------------------------User management -----------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='admin_login')
def user_mangement(request):
    users = User.objects.all().order_by('id')
    return render(request,'adminside/usermanagement/user_management.html',{'users':users})
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='admin_login')
def user_block(request,user_id):
    users = User.objects.get(id=user_id)
    if users.is_superuser:
        messages.error(request,"Cannot block superuser")
        return redirect(user_mangement)
    if users.is_active is True:
        users.is_active = False
        messages.success(request,"Un blocked successfully")
    else:
        users.is_active = True
        messages.success(request,"Blocked Successfully")
    users.save()
    return redirect(user_mangement)
    
