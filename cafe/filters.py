import django_filters

from cafe.models import Order


class OrdersFilter(django_filters.FilterSet):
    date_range = django_filters.DateRangeFilter(field_name='Date range')

    class Meta:
        model = Order
        fields = [
            'employee',
            'order_status',
            'payment_type',
            'shop'
        ]
