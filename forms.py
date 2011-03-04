from django import forms
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
import hashlib
from django.utils.translation import ugettext_lazy as _
class LoginForm(forms.Form):
    username = forms.RegexField(max_length = 10,regex=r'^[1-9][0-9]{9}')
    password = forms.CharField(widget =forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length = 25)
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.RegexField(regex=r'^[1-9][0-9]{9}@daiict.ac.in')
    password1 = forms.CharField(widget = forms.PasswordInput)
    password2 = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = User
        fields = ("username",)
    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username = username)
        except User.DoNotExist:
            return username
        raise forms.validationError(_("A user with that username already exists. "))
    def clean_password(self):
        try:
            password1 = self.cleaned_data["password1"]
        except KeyError:
            raise forms.validationError(_("The two password fields didn't match."))
        password2 = self.cleaned_data["password2"]    
        if password1 != password2: 
            raise forms.validationError(_("The two password fields didn't match."))
        return password2    

    def save(self, commit=True):
        user = super(UserCreationForm,self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.set_email(self.cleaned_data["email"])
        user.set_first_name(self.cleaned_data["first_name"])
        user.set_last_name(slef.cleaned_data["last_name"])

        if commit:
            user.save()
        return user


    
