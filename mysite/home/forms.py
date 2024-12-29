from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UploadFileForm(forms.Form):
    file = forms.FileField()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['hostel', 'room', 'image']

class lib_ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class lib_UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name','email']