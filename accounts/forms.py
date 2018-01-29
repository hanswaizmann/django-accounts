from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import ugettext_lazy as _

from .models import User, UserProfile 

class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2')


class PasswordChangeCustomForm(PasswordChangeForm):
    old_password  = forms.CharField(label=_('Old Password'), widget=forms.PasswordInput)
    new_password1 = forms.CharField(label=_('New Password'), widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_('Repeat New Password'), widget=forms.PasswordInput)

class UpdateUserProfile(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['www', 'desc', 'first_name', 'last_name' ]

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", )

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'www', 'desc' )

class UserProfileSignUpForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("first_name", "last_name")
