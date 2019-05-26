from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from cafe.models import Table
from users.forms import CustomUserCreationForm, SalaryForm, ScheduleForm
from users.models import Employee, Booking, Client, Salary, Schedule

User = get_user_model()


class EmployeeInline(admin.StackedInline):
    verbose_name_plural = _('employee info')
    verbose_name = _('Type')
    model = Employee
    can_delete = False
    readonly_fields = ('cafe',)


class ClientInline(admin.StackedInline):
    model = Client


class TableInline(admin.StackedInline):
    model = Table
    extra = 1


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm

    list_display = ('username', 'last_name', 'first_name', 'type', 'is_active')
    ordering = ('-date_joined', 'username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone', 'type')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('username',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone')}),
    )
    readonly_fields = ('last_login', 'date_joined', 'type')
    inlines = (EmployeeInline, ClientInline)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'user')
    autocomplete_fields = ('tables',)


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    form = SalaryForm
    list_display = ('user', 'amount', 'date')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    form = ScheduleForm
    list_display = ('user', 'shop', 'week_day', 'start_time', 'end_time')
    autocomplete_fields = ('shop',)
