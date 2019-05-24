from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from users.models import Employee, Client

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'placeholder': "Password"})
    )
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput(attrs={'placeholder': "Confirm"})
    )
    phone = forms.CharField(widget=forms.NumberInput())

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Client.objects.filter(email=email):
            raise forms.ValidationError(_("Email already in use"))
        return email

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'password2', 'email', 'phone')


class CustomUserCreationForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

