from django import forms
from django.contrib.auth import get_user_model

from cafe.models import Order

User = get_user_model()


class OrderForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=User.objects.filter(employee__isnull=False), label='Employee')
    client = forms.ModelChoiceField(queryset=User.objects.filter(employee__isnull=True), label='Client')

    class Meta:
        model = Order
        fields = '__all__'
