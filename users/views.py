from datetime import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, ListView

from cafe.filters import ScheduleFilter
from cafe.models import Table
from users.forms import RegisterForm, BookingForm, AddScheduleForm, AddAdminScheduleForm
from users.models import Client, Booking, Schedule, Employee
from users.utils import AnonymousRequiredMixin, EmployeeRequiredMixin, AdminRequiredMixin

User = get_user_model()


class RegisterView(AnonymousRequiredMixin, FormView):
    template_name = 'users/registration.html'
    form_class = RegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        form.cleaned_data.pop('password2')
        user = User.objects.create_user(**form.cleaned_data, is_active=True)
        Client.objects.create(email=form.cleaned_data['email'], user=user)
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
        booking.tables.set(shop_tables[:2])
        messages.success(request=self.request, message='Reservation successfully created', extra_tags='success')
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors['__all__'].data[0].messages:
            messages.error(request=self.request, message=error, extra_tags='error')
        return HttpResponseRedirect(self.get_success_url())


class ScheduleListView(EmployeeRequiredMixin, ListView):
    template_name = 'users/schedules.html'

    def get_queryset(self):
        return ScheduleFilter(self.request.GET, queryset=Schedule.objects.filter(
            user=self.request.user, approve_date__isnull=False))\
            if self.request.user.employee.job_title != Employee.ADMIN else ScheduleFilter(
            self.request.GET, queryset=Schedule.objects.all())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update({'form': AddAdminScheduleForm if self.request.user.employee.job_title == Employee.ADMIN else AddScheduleForm})
        return context


class AddScheduleView(EmployeeRequiredMixin, FormView):
    http_method_names = ['post']
    success_url = reverse_lazy('users:schedules')
    form_class = AddScheduleForm

    def form_valid(self, form):
        schedules = Schedule.objects.filter(user=self.request.user).filter(Q(start_time__range=[form.cleaned_data['start_time'], form.cleaned_data['end_time']]) | Q(end_time__range=[form.cleaned_data['start_time'], form.cleaned_data['end_time']]))
        if schedules:
            messages.error(request=self.request, message='Schedule conflict!', extra_tags='error')
            return HttpResponseRedirect(self.get_success_url())
        Schedule.objects.create(user=self.request.user, **form.cleaned_data)
        messages.success(request=self.request, message='Schedule successfully created', extra_tags='success')
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors['__all__'].data[0].messages:
            messages.error(request=self.request, message=error, extra_tags='error')
        return HttpResponseRedirect(self.get_success_url())


class UpdateScheduleView(EmployeeRequiredMixin, FormView):
    http_method_names = ['post']
    success_url = reverse_lazy('users:schedules')

    def post(self, request, *args, **kwargs):
        schedule = get_object_or_404(Schedule, pk=kwargs.get('pk'))
        if request.POST.get('change') == 'Cancel':
            schedule.delete()
            messages.success(request=self.request, message='Schedule successfully deleted', extra_tags='success')
        else:
            schedule.approve_date = datetime.today().date()
            schedule.save()
            messages.success(request=self.request, message='Schedule successfully updated', extra_tags='success')
        return HttpResponseRedirect(self.success_url)


class AddScheduleManagerView(AdminRequiredMixin, FormView):
    http_method_names = ['post']
    success_url = reverse_lazy('users:schedules')
    form_class = AddAdminScheduleForm

    def form_valid(self, form):
        schedules = Schedule.objects.filter(user=form.cleaned_data.get('user')).filter(Q(start_time__range=[form.cleaned_data['start_time'], form.cleaned_data['end_time']]) | Q(end_time__range=[form.cleaned_data['start_time'], form.cleaned_data['end_time']]))
        if schedules:
            messages.error(request=self.request, message='Employee is busy then', extra_tags='error')
            return HttpResponseRedirect(self.get_success_url())
        Schedule.objects.create(**form.cleaned_data, approve_date=datetime.now())
        messages.success(request=self.request, message='Schedule successfully created', extra_tags='success')
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors['__all__'].data[0].messages:
            messages.error(request=self.request, message=error, extra_tags='error')
        return HttpResponseRedirect(self.get_success_url())
