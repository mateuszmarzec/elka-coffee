from django.contrib.auth import views
from django.urls import path

from users.views import RegisterView, IndexView

app_name = 'users'
urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('registration', RegisterView.as_view(), name="register"),
    path(r'login', views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path(r'logout', views.LoginView.as_view(), name='logout'),
]
