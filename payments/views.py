from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from .models import PaymentLog


class PaymentHistoryView(ListView):
    template_name = 'payments/history.html'
    queryset = PaymentLog.objects.all()

    def get_queryset(self):
        return PaymentLog.objects.filter(enrolled__in=self.request.user.enrolled_courses.all())

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)