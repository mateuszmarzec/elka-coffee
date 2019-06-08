import django_filters

from cafe.models import Order


class OrdersFilter(django_filters.FilterSet):
    date_range = django_filters.DateRangeFilter(field_name='timestamp')

    class Meta:
        model = Order
        fields = [
            'employee',
            'order_status',
            'payment_type',
            'shop'
        ]
