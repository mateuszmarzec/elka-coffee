from django.contrib import admin

from cafe.models import Shop, Cafe, Address, Table
from users.admin import TableInline


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'close_time', 'address')
    autocomplete_fields = ('address',)
    exclude = ('cafe',)
    inlines = (TableInline,)


@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'address')
    autocomplete_fields = ('address',)
    readonly_fields = ('name',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('city', 'street', 'postal_code')
    search_fields = ('street', 'city')


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('shop', 'number', 'max_seats',)
    search_fields = ('shop', 'number')
