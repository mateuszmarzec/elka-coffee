from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.http import Http404


class AnonymousRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class EmployeeRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        if not request.user.employee:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
