# from django import forms
# from .models import UserProfile
# from django.contrib.auth.forms import UserCreationForm

# class Signup_form(UserCreationForm):
#     class Meta:
#         model= UserProfile
#         fields = ['username','first_name','last_name','email','phone_number']
    
#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         if UserProfile.objects.filter(username=username).exists():
#             raise forms.ValidationError('This Username already exists.') 
#         return username
    
#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         if username.strip()=='':
#             raise forms.ValidationError('Enter username.') 
#         return username

#     def clean_first_name(self):
#         first_name = self.cleaned_data.get('first_name')
#         if first_name.strip()=='':
#             raise forms.ValidationError('Enter first name.') 
#         return first_name
    
#     def clean_last_name(self):
#         last_name = self.cleaned_data.get('last_name')
#         if last_name.strip()=='':
#             raise forms.ValidationError('Enter last name.') 
#         return last_name

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if UserProfile.objects.filter(email=email).exists():
#             raise forms.ValidationError('This email address is already registered.') 
#         return email

#     # def clean_phone_number(self):
#     #     phone_number = self.cleaned_data.get('phone_number') 
#     #     if UserProfile.objects.filter(phone_number=phone_number).exists():
#     #         raise forms.ValidationError('This Phone number is already registered.') 
#     #     return phone_number 
    
#     def clean_password1(self):
#         password1 = self.cleaned_data.get('password1')
#         if password1.strip()=='':
#             raise forms.ValidationError('Enter password.') 
#         return password1


#     def clean(self):
#         cleaned_data = super().clean()
#         password1 = cleaned_data.get('password1') 
#         password2 = cleaned_data.get('password2') 

#         if password1 and password2 and password1!=password2:
#              self.add_error('password2', 'The passwords do not match.')
#         return cleaned_data