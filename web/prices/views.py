from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import UpdateView, CreateView, DetailView
from django.urls import reverse, reverse_lazy
from django.shortcuts import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from .models import PriceModel
from .forms import PriceForm
from django.utils import timezone
from lib.templatetags.permissions import requires_business_owner_or_app_staff
from services.models import ServiceModel


@method_decorator(requires_business_owner_or_app_staff, name='dispatch')
class PriceServiceUpdateView(SuccessMessageMixin, UpdateView):

    form_class = PriceForm
    model = PriceModel
    context_object_name = 'price'
    template_name = 'prices/price_service_update.html'
    success_message = "Alterações realizadas com sucesso!"

    def get_context_data(self, **kwargs):

        context = super(PriceServiceUpdateView, self).get_context_data(**kwargs)
        context['business_slug'] = self.kwargs.get('slug')
        service = ServiceModel.objects.get(slug=self.kwargs.get('service_slug'))
        context['service'] = service
        self.request.session['service_slug'] = service.slug
        return context

    def form_valid(self, form):
        form.instance.service = ServiceModel.objects.get(slug=self.kwargs.get('service_slug'))
        form.instance.old_value = form.instance.value_tracker.previous('price_value')
        form.instance.updated_at = timezone.now()
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        business = self.kwargs.get('slug')
        service = self.kwargs.get('service_slug')
        if 'service_session' in self.request.session:
            return reverse_lazy("service_equipment_create", kwargs={'slug': business, 'service_slug': service})
        else:
            return reverse_lazy('service_detail', kwargs={'slug': business, 'service_slug': service})
