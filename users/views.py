from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, ListView

from cafe.models import Table
from users.forms import RegisterForm, BookingForm
from users.models import Client, Booking
from users.utils import AnonymousRequiredMixin

User = get_user_model()


class RegisterView(AnonymousRequiredMixin, FormView):
    template_name = 'users/registration.html'
    form_class = RegisterForm
    success_url = reverse_lazy("users:login")

    @transaction.atomic
    def form_valid(self, form):
        form.cleaned_data.pop('password2')
        client = Client.objects.create(email=form.cleaned_data['email'])
        User.objects.create_user(**form.cleaned_data, is_active=True, client=client)
        return super().form_valid(form)


class LoginView(AnonymousRequiredMixin, LoginView):
    pass


class IndexView(TemplateView):
    template_name = 'index.html'


class BookingListView(LoginRequiredMixin, ListView):
    template_name = 'users/bookings.html'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update({'form': BookingForm})
        return context


class CreateBookingView(LoginRequiredMixin, FormView):
    http_method_names = ['post']
    success_url = reverse_lazy('users:bookings')
    form_class = BookingForm

    @transaction.atomic
    def form_valid(self, form):
        booking = Booking.objects.create(
            user=self.request.user, end_time=form.cleaned_data.get('end_time'),
            start_time=form.cleaned_data.get('start_time')
        )
        number_of_guests = form.cleaned_data.get('number_of_guests')
        shop_tables = Table.objects.filter(shop=form.cleaned_data.get('shop')).exclude(
            bookings__start_time__range=[form.cleaned_data.get('start_time'), form.cleaned_data.get('end_time')],
            bookings__end_time__range=[form.cleaned_data.get('start_time'), form.cleaned_data.get('end_time')],
        )
        booking.tables.set(shop_tables)
        messages.success(request=self.request, message='Reservation successfully created', extra_tags='success')
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors['__all__'].data[0].messages:
            messages.error(request=self.request, message=error, extra_tags='error')
        return HttpResponseRedirect(self.get_success_url())
