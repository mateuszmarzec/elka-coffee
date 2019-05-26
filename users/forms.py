import datetime

from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput, TimePickerInput
from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.forms import ModelForm, Form
from django.utils.translation import ugettext_lazy as _

from cafe.models import Shop, Table
from users.models import Client, Salary, Schedule

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


class BookingForm(Form):
    shop = forms.ModelChoiceField(queryset=Shop.objects.all(), required=True, label='Coffeehouse', initial=1)
    number_of_guests = forms.IntegerField(required=True, label='How many seats you need', initial=5)
    date = forms.DateField(required=True, widget=DatePickerInput(format='%m/%d/%Y'))
    start_time = forms.TimeField(required=True, widget=TimePickerInput(format='H:m'))
    end_time = forms.TimeField(required=True, widget=TimePickerInput(format='H:m'))

    def clean_start_time(self):
        date = self.cleaned_data.get('date')
        start_time = self.cleaned_data.get('start_time')
        return datetime.datetime(
            year=date.year, month=date.month, day=date.day, hour=start_time.hour, minute=start_time.minute
        )

    def clean_end_time(self):
        date = self.cleaned_data.get('date')
        end_time = self.cleaned_data.get('end_time')
        return datetime.datetime(
            year=date.year, month=date.month, day=date.day, hour=end_time.hour, minute=end_time.minute
        )

    def clean(self):
        if self.cleaned_data.get('start_time') > self.cleaned_data.get('end_time'):
            raise forms.ValidationError('Start time can\'t be later than end time')

        available_tables = Table.objects.filter(shop=self.cleaned_data.get('shop')).exclude(
            bookings__start_time__range=[self.cleaned_data.get('start_time'), self.cleaned_data.get('end_time')],
            bookings__end_time__range=[self.cleaned_data.get('start_time'), self.cleaned_data.get('end_time')],
        )
        if not available_tables or available_tables.aggregate(Sum('max_seats'))['max_seats__sum'] < self.cleaned_data.get('number_of_guests'):
            raise forms.ValidationError('No tables available in this coffeehouse for given date')


class SalaryForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(employee__isnull=False), label='Employee')

    class Meta:
        model = Salary
        fields = '__all__'


class ScheduleForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(employee__isnull=False), label='Employee')

    class Meta:
        model = Schedule
        fields = '__all__'
