from django.contrib.auth import get_user_model
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from users.forms import RegisterForm
from users.models import Client

User = get_user_model()


class RegisterView(FormView):
    template_name = 'users/registration.html'
    form_class = RegisterForm
    success_url = reverse_lazy("users:login")

    @transaction.atomic
    def form_valid(self, form):
        form.cleaned_data.pop('password2')
        client = Client.objects.create(email=form.cleaned_data['email'])
        User.objects.create_user(**form.cleaned_data, is_active=True, client=client)
        return super().form_valid(form)


class IndexView(TemplateView):
    template_name = 'index.html'
