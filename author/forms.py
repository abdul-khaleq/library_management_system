from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .import models

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'id' : 'required'}))
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        
    def save(self,commit=True):
        our_user = super().save(commit=False)
        if commit== True:
            our_user.save()
            
            models.UserModel.objects.create(
                user = our_user
            )
        return our_user
    
# class RegistrationForm(UserCreationForm):
#     first_name = forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))
#     last_name = forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))

#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email']

class ChangeUserForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class DepositForm(forms.Form):
    amount = forms.IntegerField(label='Amount',required=True)


