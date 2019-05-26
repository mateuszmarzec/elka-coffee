from datetime import datetime

from django.views.generic import ListView, TemplateView

from cafe.models import Shop, Cafe, Menu


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
