from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    phone = models.CharField(max_length=12, blank=True)

    @property
    def type(self):
        return 'client' if self.client else 'employee'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return str(self.get_full_name())


class Employee(models.Model):
    ADMIN = 'admin'
    BARISTA = 'barista'
    CASHIER = 'cashier'

    JOB_CHOICES = (
        (ADMIN, 'Admin'),
        (BARISTA, 'Barista'),
        (CASHIER, 'Cashier'),
    )

    account_number = models.CharField(max_length=26, blank=True)
    job_title = models.CharField(max_length=20, blank=True, choices=JOB_CHOICES)
    user = models.OneToOneField(to='User', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')

    def __str__(self):
        return str("{}".format(self.get_job_title_display()))


class Client(models.Model):
    email = models.EmailField(max_length=50, unique=True)
    user = models.OneToOneField(to='User', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _('client')
        verbose_name_plural = _('clients')

    def __str__(self):
        return str("{}".format(self.email))
