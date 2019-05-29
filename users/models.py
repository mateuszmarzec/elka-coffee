from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    phone = models.CharField(max_length=12, blank=True)

    @property
    def type(self):
        return 'client' if hasattr(self, 'client') else 'employee'

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
    BARIST = 'barist'
    CASHIER = 'cashier'

    JOB_CHOICES = (
        (ADMIN, 'Admin'),
        (BARIST, 'Barist'),
        (CASHIER, 'Cashier'),
    )

    account_number = models.CharField(max_length=26, blank=True)
    job_title = models.CharField(max_length=20, blank=True, choices=JOB_CHOICES)
    user = models.OneToOneField(to='User', on_delete=models.CASCADE)
    cafe = models.ForeignKey(to='cafe.Cafe', on_delete=models.SET_NULL, default=1, null=True)

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


class Booking(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(to='User', on_delete=models.CASCADE)
    tables = models.ManyToManyField(to='cafe.Table', related_name='bookings')

    class Meta:
        verbose_name = _('booking')
        verbose_name_plural = _('bookings')
        ordering = ('-start_time', '-end_time')

    def __str__(self):
        return str("{} {} - {}".format(self.user, self.start_time, self.end_time))


class Salary(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=7)
    date = models.DateField()
    user = models.ForeignKey(to='User', on_delete=models.CASCADE, )

    class Meta:
        ordering = ('-date',)
        verbose_name = _('salary')
        verbose_name_plural = _('salaries')

    def __str__(self):
        return str("{} {}".format(self.user, self.amount))


class Schedule(models.Model):
    MONDAY = 'monday'
    TUESDAY = 'tuesday'
    WEDNESDAY = 'wednesday'
    THURSDAY = 'thursday'
    FRIDAY = 'friday'
    SATURDAY = 'saturday'
    SUNDAY = 'sunday'

    DAYS_OF_WEEK = (
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    )
    week_day = models.CharField(max_length=20, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    approve_date = models.DateField(null=True, blank=True)
    shop = models.ForeignKey(to='cafe.Shop', on_delete=models.CASCADE)
    user = models.ForeignKey(to='User', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _('schedule')
        verbose_name_plural = _('schedules')
        ordering = ('-id',)

    def __str__(self):
        return str("{} {} {}".format(self.week_day, self.user, self.shop))


@receiver(post_save, sender=User)
def set_is_superuser(sender, instance, **kwargs):
    if hasattr(instance, 'employee') and instance.employee.job_title == Employee.ADMIN:
        sender.objects.filter(id=instance.id).update(is_superuser=True, is_staff=True)
