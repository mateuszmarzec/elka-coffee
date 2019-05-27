from datetime import datetime

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


class Cafe(models.Model):
    name = models.CharField(max_length=30, unique=True)
    phone_number = models.CharField(max_length=13, unique=True)
    email = models.EmailField(max_length=30, unique=True)
    address = models.OneToOneField(to='Address', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('cafe')
        verbose_name_plural = _('cafes')


class Address(models.Model):
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    building_number = models.PositiveIntegerField()
    apartment_number = models.PositiveIntegerField(null=True, blank=True)
    postal_code = models.CharField(max_length=6)

    def __str__(self):
        return '{} {} {}{}'.format(
            self.city, self.street, self.building_number, '/'+str(self.apartment_number) if self.apartment_number else ''
        )

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')


class Shop(models.Model):
    name = models.CharField(max_length=30, unique=True)
    start_time = models.TimeField()
    close_time = models.TimeField()
    phone_number = models.CharField(max_length=13, unique=True)
    email = models.EmailField(max_length=30, unique=True)
    address = models.OneToOneField(to='Address', on_delete=models.SET_NULL, null=True, blank=True)
    cafe = models.ForeignKey(to='Cafe', on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(blank=True)
    ingredients = models.ManyToManyField(to='Ingredient', through='StorageState', related_name='shops')

    def __str__(self):
        return '{} {}'.format(self.name, self.address)

    class Meta:
        verbose_name = _('shop')
        verbose_name_plural = _('shops')


class Table(models.Model):
    shop = models.ForeignKey(to='Shop', on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    max_seats = models.PositiveIntegerField()

    class Meta:
        unique_together = ('shop', 'number')
        verbose_name = _('table')
        verbose_name_plural = _('tables')

    def __str__(self):
        return '{} number : {} max seats: {}'.format(self.shop, self.number, self.max_seats)


class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    cafe = models.ForeignKey(to='Cafe', on_delete=models.CASCADE, default=1)
    products = models.ManyToManyField(to='Product', related_name='menus')

    class Meta:
        verbose_name = _('menu')
        verbose_name_plural = _('menus')
        ordering = ('-start_date', '-end_date')

    def __str__(self):
        return self.name

    @property
    def is_current(self):
        return self.start_date <= datetime.today() and self.end_date <= datetime.today()


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True)
    ingredients = models.ManyToManyField(to='Ingredient', through='ProductIngredient', related_name='products')

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return '{} ({} PLN)'.format(self.name, self.price)


class ProductIngredient(models.Model):
    product = models.ForeignKey(to='Product', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(to='Ingredient', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)


class StorageState(models.Model):
    shop = models.ForeignKey(to='Shop', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(to='Ingredient', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        unique_together = ('shop', 'ingredient')


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    unit_type = models.ForeignKey(to='UnitType', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _('ingredient')
        verbose_name_plural = _('ingredients')

    def __str__(self):
        return '{} ({})'.format(self.name, self.unit_type)


class UnitType(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = _('unit type')
        verbose_name_plural = _('unit types')

    def __str__(self):
        return self.name


class Order(models.Model):
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(
        to='users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='order_by'
    )
    employee = models.ForeignKey(
        to='users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='accepted_by'
    )
    products = models.ManyToManyField(to='Product', related_name='orders')
    shop = models.ForeignKey(to='Shop', on_delete=models.CASCADE, null=True, blank=True)
    order_status = models.ForeignKey(to='OrderStatus', on_delete=models.SET_NULL, null=True)
    payment_type = models.ForeignKey(to='PaymentType', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ('-timestamp',)

    def __str__(self):
        return '{} {} {} {}'.format(self.amount, self.client, self.payment_type, self.payment_type)


class OrderStatus(models.Model):
    status = models.CharField(max_length=20)

    class Meta:
        verbose_name = _('order status')
        verbose_name_plural = _('order statuses')

    def __str__(self):
        return self.status


class PaymentType(models.Model):
    type = models.CharField(max_length=50)

    class Meta:
        verbose_name = _('payment type')
        verbose_name_plural = _('payment types')

    def __str__(self):
        return self.type


class Supply(models.Model):
    date = models.DateField()
    description = models.TextField(blank=True)
    shop = models.ForeignKey(to='Shop', on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(to='Ingredient', through='SuppliedIngredient', related_name='supplies')

    class Meta:
        ordering = ('-date',)
        verbose_name = _('supply')
        verbose_name_plural = _('supplies')

    def __str__(self):
        return ''.format(self.date, self.shop)


class SuppliedIngredient(models.Model):
    supply = models.ForeignKey(to='Supply', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(to='Ingredient', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()


@receiver(post_save, sender=Shop)
def set_cafe(sender, instance, **kwargs):
    sender.objects.filter(id=instance.id).update(cafe=Cafe.objects.first())
