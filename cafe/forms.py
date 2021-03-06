from datetime import datetime

from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django.contrib.auth import get_user_model
from django.forms import formset_factory, inlineformset_factory

from cafe.models import Order, Shop, StorageState, Menu, Supply, SuppliedIngredient

User = get_user_model()


class OrderForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=User.objects.filter(employee__isnull=False), label='Employee', required=True)
    client = forms.ModelChoiceField(queryset=User.objects.filter(employee__isnull=True), label='Client', required=True)

    class Meta:
        model = Order
        fields = '__all__'


class CreateOrderForm(forms.ModelForm):
    shop = forms.ModelChoiceField(queryset=Shop.objects.all(), label='Coffeehouse', required=True)
    products = forms.ModelMultipleChoiceField(
        queryset=Menu.objects.filter(start_date__lte=datetime.today(), end_date__gte=datetime.today()).last().products
    )

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


class SupplyIngredientForm(forms.ModelForm):
    amount = forms.IntegerField(required=True)

    class Meta:
        model = SuppliedIngredient
        exclude = ('supply',)


SupplyIngredientFormSet = formset_factory(
    form=SupplyIngredientForm, extra=1, can_delete=False
)


class SupplyForm(forms.ModelForm):
    ingredients = formset_factory(SupplyIngredientForm)

    class Meta:
        model = Supply
        exclude = ('date', 'ingredients')


class FilterForm(forms.Form):
    shop = forms.ModelChoiceField(queryset=Shop.objects.all(), label='Coffeehouse', required=False)
    start_date = forms.DateField(widget=DatePickerInput(format='%m/%d/%Y'), label="From", required=False)
    end_date = forms.DateField(widget=DatePickerInput(format='%m/%d/%Y'), label="To", required=False)
