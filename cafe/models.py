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
        return '{} {} {} {}'.format(
            self.city, self.street, self.building_number, self.apartment_number if self.apartment_number else ''
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


@receiver(post_save, sender=Shop)
def set_cafe(sender, instance, **kwargs):
    sender.objects.filter(id=instance.id).update(cafe=Cafe.objects.first())
