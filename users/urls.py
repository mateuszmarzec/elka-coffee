from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.urls import path

from cafe.views import SupplyListView, SalaryListView, AddSalaryView, ProductOrderReportView, ReportsView, \
    EmployeeOrderReportView, IngredientUsageReportView
from users.views import RegisterView, IndexView, LoginView, BookingListView, CreateBookingView, ScheduleListView, \
    AddScheduleView, UpdateScheduleView, AddScheduleManagerView

app_name = 'users'
urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('registration', RegisterView.as_view(), name="register"),
    path('my-reservations', BookingListView.as_view(), name="bookings"),
    path('schedules', ScheduleListView.as_view(), name="schedules"),
    path('add-schedules', AddScheduleView.as_view(), name="add-schedules"),
    path('add-manager-schedules', AddScheduleManagerView.as_view(), name="add-manager-schedules"),
    path('update-schedules/<int:pk>', UpdateScheduleView.as_view(), name="update-schedules"),
    path('add-reservations', CreateBookingView.as_view(), name="add-booking"),
    path('supplies', SupplyListView.as_view(), name="supplies"),
    path('salary', SalaryListView.as_view(), name="salaries"),
    path('add-salary', AddSalaryView.as_view(), name="add-salary"),
    path('reports', ReportsView.as_view(), name="reports"),
    path('reports/product-order-report', ProductOrderReportView.as_view(), name="order-report"),
    path('reports/employee-order-report', EmployeeOrderReportView.as_view(), name="employee-order-report"),
    path('reports/ingredient-report', IngredientUsageReportView.as_view(), name="ingredient-report"),
    path(r'login', LoginView.as_view(template_name='users/login.html'), name='login'),
    path(r'logout', login_required(views.LogoutView.as_view()), name='logout'),
]
