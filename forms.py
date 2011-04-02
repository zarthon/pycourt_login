from django import forms
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
import hashlib
from django.utils.translation import ugettext_lazy as _
from pycourt_login.models import Dishes
class ResetForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_password2(self):
        try:
            password1 = self.cleaned_data["password1"]
        except KeyError:
            raise forms.ValidationError(_("The two password fields didn't match."))
        password2 = self.cleaned_data["password2"] 
        if password1 != password2: 
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2    


class ForgotForm(forms.Form):
    username = forms.RegexField(max_length = 10, regex=r'^[1-9][0-9]{8}')
    class Meta:
        model = User
        fields = ("username",)
    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(_("The specified Username does not exist"))

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 10)
    password = forms.CharField(widget =forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    username = forms.RegexField(max_length = 25,regex=r'^[1-9][0-9]{8}')
    first_name = forms.CharField(max_length = 60)
    last_name = forms.CharField(max_length=60)
    email = forms.RegexField(regex=r'^[1-9][0-9]{8}@daiict.ac.in')
    password1 = forms.CharField(widget = forms.PasswordInput)
    password2 = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username = username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("A user with that username already exists. "))
    def clean_password2(self):
        try:
            password1 = self.cleaned_data["password1"]
        except KeyError:
            raise forms.ValidationError(_("The two password fields didn't match."))
        password2 = self.cleaned_data["password2"]    
        if password1 != password2: 
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2    

    def save(self, commit=True):
        user = super(RegisterForm,self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email=(self.cleaned_data["email"])
        user.first_name=(self.cleaned_data["first_name"])
        user.last_name = (self.cleaned_data["last_name"])
        if commit:
            user.save()
        return user

class SettingForm(forms.ModelForm):

    email = forms.RegexField(regex=r'^[1-9][0-9]{8}@daiict.ac.in')
    class Meta:
        model = User
        fields = ('first_name','last_name','email')


    def save(self, commit=True):
        user = super(SettingForm,self).save(commit=False)
        user.email=(self.cleaned_data["email"])
        user.first_name=(self.cleaned_data["first_name"])
        user.last_name = (self.cleaned_data["last_name"])
        if commit:
            user.save()
        return user

class AddDishForm(forms.Form):
    dishname = forms.CharField(max_length=30)
    dishprice = forms.IntegerField()
    def clean_dishname(self):
        dishname = self.cleaned_data.get("dishname")
        dishes = Dishes.objects.all()
        for dish in dishes:
            if dish.dish_name.lower().replace(" ","") == dishname.lower().replace(" ",""):
                raise forms.ValidationError(_("The specified Dish already exist"))

        return dishname
 
class RechargeForm(forms.Form):
    username = forms.RegexField(max_length = 10, regex=r'^[1-9][0-9]{8}')
    password = forms.CharField(widget = forms.PasswordInput)
    amount = forms.IntegerField()
    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username = username)
        except User.DoesNotExist:
            raise forms.ValidationError(_("The User does not exists."))
        return username 
