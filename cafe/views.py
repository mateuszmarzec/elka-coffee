from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count, Case, When, IntegerField
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, TemplateView, FormView

from cafe.filters import OrdersFilter
from cafe.forms import CreateOrderForm, SupplyForm, SupplyIngredientFormSet, FilterForm
from cafe.models import Shop, Cafe, Menu, Order, OrderStatus, StorageState, Supply, SuppliedIngredient, Product
from users.forms import AddSalaryForm
from users.models import Salary, Employee
from users.utils import EmployeeRequiredMixin, AdminRequiredMixin


class ShopsView(ListView):
    template_name = 'cafe/shops.html'
    queryset = Shop.objects.all()


class CafeView(TemplateView):
    template_name = 'cafe/cafe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(cafe=Cafe.objects.first())
        return context


class MenuView(TemplateView):
    template_name = 'cafe/menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(menu=Menu.objects.filter(
            start_date__lte=datetime.today().date(), end_date__gte=datetime.today().date()
        ).last())
        return context


class OrderListView(EmployeeRequiredMixin, ListView):
    template_name = 'cafe/orders.html'

    def get_queryset(self):
        return OrdersFilter(self.request.GET, queryset=Order.objects.filter(client__isnull=True))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update({'form': CreateOrderForm})
        return context


class OnlineOrderListView(LoginRequiredMixin, ListView):
    template_name = 'cafe/online_orders.html'

    def get_queryset(self):
        return Order.objects.filter(client__isnull=False) if hasattr(self.request.user, 'employee') else Order.objects.filter(client=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update({'form': CreateOrderForm})
        return context


class CreateOrderView(LoginRequiredMixin, FormView):
    http_method_names = ['post']
    success_url = reverse_lazy('cafe:online-orders')
    form_class = CreateOrderForm

    def get_success_url(self):
        if self.request.user.type == 'employee':
            return reverse('cafe:orders')
        return super().get_success_url()

    def form_valid(self, form):
        products = form.cleaned_data.pop('products')
        amount = products.aggregate(Sum('price'))['price__sum']
        if self.request.user.type == 'client':
            order = Order.objects.create(
                **form.cleaned_data, client=self.request.user,
                order_status=OrderStatus.objects.filter(id=1).last(),
                amount=amount
            )
        else:
            order = Order.objects.create(
                **form.cleaned_data, employee=self.request.user,
                order_status=OrderStatus.objects.filter(id=2).last(),
                amount=amount
            )
        for product in products:
            for ingredient in product.ingredients.all():
                storage = StorageState.objects.filter(shop=form.cleaned_data.get('shop'), ingredient=ingredient).last()
                if storage:
                    storage.amount = storage.amount - product.productingredient_set.get(ingredient=ingredient).amount
                    storage.save()
        order.products.set(products)
        messages.success(request=self.request, message='Order successfully made', extra_tags='success')
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors['__all__'].data[0].messages:
            messages.error(request=self.request, message=error, extra_tags='error')
        return HttpResponseRedirect(self.get_success_url())


class UpdateOrderView(EmployeeRequiredMixin, FormView):
    http_method_names = ['post']
    success_url = reverse_lazy('cafe:online-orders')

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs.get('pk'))
        if request.POST.get('change') == 'Cancel':
            order.delete()
            messages.success(request=self.request, message='Order successfully deleted', extra_tags='success')
        else:
            order.order_status_id = 2
            order.employee = request.user
            order.save()
            messages.success(request=self.request, message='Order successfully updated', extra_tags='success')
        return HttpResponseRedirect(self.success_url)


class StorageView(EmployeeRequiredMixin, ListView):
    template_name = 'cafe/storage.html'
    queryset = Shop.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update({'form': SupplyForm, 'formset': SupplyIngredientFormSet})
        return context


class CreateSupplyView(EmployeeRequiredMixin, FormView):
    http_method_names = ['post']
    success_url = reverse_lazy('cafe:storage')
    form_class = SupplyForm

    def form_valid(self, form):
        supply = Supply.objects.create(date=datetime.today().date(), **form.cleaned_data)
        formset = SupplyIngredientFormSet(self.request.POST)
        if formset.is_valid():
            for f in formset:
                SuppliedIngredient.objects.create(supply=supply, **f.cleaned_data)
                ss = StorageState.objects.filter(
                    shop=form.cleaned_data.get('shop'), ingredient=f.cleaned_data.get('ingredient')
                ).last()
                if ss:
                    ss.amount = ss.amount + f.cleaned_data.get('amount')
                    ss.save()
                else:
                    StorageState.objects.create(
                        shop=form.cleaned_data.get('shop'), ingredient=f.cleaned_data.get('ingredient'), amount=f.cleaned_data.get('amount')
                    )

            messages.success(request=self.request, message='Supply successfully ordered', extra_tags='success')
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors['__all__'].data[0].messages:
            messages.error(request=self.request, message=error, extra_tags='error')
        return HttpResponseRedirect(self.get_success_url())


class SupplyListView(AdminRequiredMixin, ListView):
    template_name = 'cafe/supplies.html'
    queryset = Supply.objects.all()
    ordering = ('-date', '-pk')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update({'form': SupplyForm, 'formset': SupplyIngredientFormSet})
        return context


class SalaryListView(EmployeeRequiredMixin, ListView):
    template_name = 'users/salaries.html'

    def get_queryset(self):
        return Salary.objects.all() if self.request.user.employee.job_title == Employee.ADMIN else Salary.objects.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update({'form': AddSalaryForm})
        return context


class AddSalaryView(AdminRequiredMixin, FormView):
    http_method_names = ['post']
    success_url = reverse_lazy('users:salaries')
    form_class = AddSalaryForm

    def form_valid(self, form):
        Salary.objects.create(**form.cleaned_data)
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors['__all__'].data[0].messages:
            messages.error(request=self.request, message=error, extra_tags='error')
        return HttpResponseRedirect(self.get_success_url())


class ReportsView(AdminRequiredMixin, TemplateView):
    template_name = 'cafe/reports.html'


class OrderReportView(AdminRequiredMixin, ListView):
    template_name = 'cafe/order-report.html'

    def get_queryset(self):
        shop = self.request.GET.get('shop')
        if shop:
            return Product.objects.annotate(
                order_count=Count(Case(When(orders__shop=shop, then=1)), output_field=IntegerField())
            )

        return Product.objects.annotate(order_count=Count('orders'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update({'filter': FilterForm})
        return context
