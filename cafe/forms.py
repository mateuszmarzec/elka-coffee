from django import forms
from django.contrib.auth import get_user_model

from cafe.models import Order, Shop, StorageState

User = get_user_model()


class OrderForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=User.objects.filter(employee__isnull=False), label='Employee', required=True)
    client = forms.ModelChoiceField(queryset=User.objects.filter(employee__isnull=True), label='Client', required=True)

    class Meta:
        model = Order
        fields = '__all__'


class CreateOrderForm(forms.ModelForm):
    shop = forms.ModelChoiceField(queryset=Shop.objects.all(), label='Coffeehouse', required=True)

    class Meta:
        model = Order
        exclude = ('client', 'employee', 'order_status', 'amount')

    def clean(self):
        products = self.cleaned_data.get('products')
        for product in products:
            for ingredient in product.ingredients.all():
                storage = StorageState.objects.filter(shop=self.cleaned_data.get('shop'), ingredient=ingredient).last()
                if storage:
                    storage.amount = storage.amount - product.productingredient_set.get(ingredient=ingredient).amount
                    if storage.amount > 0:
                        return super().clean()
                raise forms.ValidationError('Not enough ingredients to prepare these products ({})'.format(ingredient.name))
