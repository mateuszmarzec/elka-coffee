from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.urls import path

from cafe.views import SupplyListView
from users.views import RegisterView, IndexView, LoginView, BookingListView, CreateBookingView, ScheduleListView, \
    AddScheduleView, UpdateScheduleView

app_name = 'users'
urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('registration', RegisterView.as_view(), name="register"),
    path('my-reservations', BookingListView.as_view(), name="bookings"),
    path('schedules', ScheduleListView.as_view(), name="schedules"),
    path('add-schedules', AddScheduleView.as_view(), name="add-schedules"),
    path('update-schedules/<int:pk>', UpdateScheduleView.as_view(), name="update-schedules"),
    path('add-reservations', CreateBookingView.as_view(), name="add-booking"),
    path('supplies', SupplyListView.as_view(), name="supplies"),
    path(r'login', LoginView.as_view(template_name='users/login.html'), name='login'),
    path(r'logout', login_required(views.LogoutView.as_view()), name='logout'),
]
