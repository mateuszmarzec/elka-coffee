from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, TemplateView, FormView

from cafe.forms import CreateOrderForm
from cafe.models import Shop, Cafe, Menu, Order, OrderStatus, StorageState
from users.utils import EmployeeRequiredMixin


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
        return Order.objects.filter(client__isnull=True)

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
