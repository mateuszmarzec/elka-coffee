from django.urls import path

from cafe.views import ShopsView, CafeView, MenuView

app_name = 'cafe'
urlpatterns = [
    path('coffeehouses', ShopsView.as_view(), name="shops"),
    path('about-us', CafeView.as_view(), name="cafe"),
    path('menu', MenuView.as_view(), name="menu"),
]
