from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.urls import path

from users.views import RegisterView, IndexView, LoginView

app_name = 'users'
urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('registration', RegisterView.as_view(), name="register"),
    path(r'login', LoginView.as_view(template_name='users/login.html'), name='login'),
    path(r'logout', login_required(views.LogoutView.as_view()), name='logout'),
]
