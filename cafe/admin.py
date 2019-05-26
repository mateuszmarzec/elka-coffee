from django.contrib import admin

from cafe.models import Shop, Cafe, Address, Table, Menu, Product, Ingredient, UnitType
from users.admin import TableInline


class IngredientInline(admin.TabularInline):
    model = Product.ingredients.through
    extra = 1


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'close_time', 'address')
    autocomplete_fields = ('address',)
    exclude = ('cafe',)
    inlines = (TableInline,)
    search_fields = ('name',)


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


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    search_fields = ('name',)
    autocomplete_fields = ('products',)
    readonly_fields = ('cafe',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)
    search_fields = ('name',)
    inlines = (IngredientInline,)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_type',)
    search_fields = ('name', 'unit_type')


@admin.register(UnitType)
class UnitTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
