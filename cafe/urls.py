from django.urls import path

from cafe.views import ShopsView, CafeView, MenuView, UpdateOrderView, \
    OnlineOrderListView, OrderListView, CreateOrderView, StorageView

app_name = 'cafe'
urlpatterns = [
    path('coffeehouses', ShopsView.as_view(), name="shops"),
    path('about-us', CafeView.as_view(), name="cafe"),
    path('menu', MenuView.as_view(), name="menu"),
    path('online-orders', OnlineOrderListView.as_view(), name="online-orders"),
    path('orders', OrderListView.as_view(), name="orders"),
    path('add-order', CreateOrderView.as_view(), name="add-order"),
    path('change-order/<int:pk>', UpdateOrderView.as_view(), name="change-order"),
    path('storage', StorageView.as_view(), name="storage"),
]
