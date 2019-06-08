import django_filters

from cafe.models import Order, Shop


class OrdersFilter(django_filters.FilterSet):
    shop = django_filters.ModelChoiceFilter(queryset=Shop.objects.all(), label='Coffeehouse')
    date_range = django_filters.DateRangeFilter(label='Date range', field_name='timestamp')

    class Meta:
        model = Order
        fields = [
            'employee',
            'order_status',
            'payment_type',
            'shop'
        ]
