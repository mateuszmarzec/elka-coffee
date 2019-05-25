from django.contrib.auth.mixins import AccessMixin
from django.http import Http404


class AnonymousRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
