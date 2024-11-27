from django import forms
from django.contrib.auth.models import User
from .models import*

class Registerform(forms.ModelForm):
    profile = forms.ImageField(required=False)
    username = forms.CharField(label='username',widget=forms.TextInput)
    email = forms.EmailField(label='email',required=True)
    password = forms.CharField(label='password',widget=forms.PasswordInput)
    cpassword = forms.CharField(label='confirm password',widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['profile','username','email','password','cpassword']


# profile update form

class Profile_update_form(forms.ModelForm):
    profile = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = ['profile','username','email']
        excluded=['password','cpassword']


