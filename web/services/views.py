import os
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import HttpResponseRedirect, Http404, get_object_or_404
from formtools.wizard.views import SessionWizardView
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from lib.templatetags.permissions import requires_business_owner_or_app_staff
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from businesses.models import BusinessModel, BusinessAddressModel, BusinessLogoQrcodeModel
from prices.models import PriceModel, get_service_equipment_time_and_price_in_list
from .models import (ServiceCategoryModel,
                     ServiceModel,
                     EquipmentModel,
                     ServiceEquipmentModel,
                     EquipmentAddressModel,
                     get_service_equipment,
                     get_service_equipment_time,
                     get_service_equipment_time_list,
                     )
from .serializers import (ServiceCategorySerializer,
                          ServiceSerializer,
                          EquipmentSerializer,
                          ServiceEquipmentSerializer,
                          EquipmentAddressSerializer,)
from .forms import (ServiceCategoryForm,
                    ServiceFormOne,
                    ServiceFormTwo,
                    EquipmentForm,
                    ServiceEquipmentForm,
                    EquipmentAddressForm,
                    )


class ServiceCategoryViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        business = self.kwargs['slug']
        service_category = ServiceCategoryModel.objects.filter(business__slug=business)
        serializer = ServiceCategorySerializer(service_category, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ServiceCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        service_category = ServiceCategoryModel.objects.get(slug=kwargs['service_category_slug'])
        serializer = ServiceCategorySerializer(instance=service_category)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        service_category = ServiceCategoryModel.objects.get(slug=kwargs['service_category_slug'])
        serializer = ServiceCategorySerializer(instance=service_category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        service_category = ServiceCategoryModel.objects.get(slug=kwargs['service_category_slug'])
        service_category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(requires_business_owner_or_app_staff, name='dispatch')
class ServiceCategoryCreateView(SuccessMessageMixin, CreateView):
    model = ServiceCategoryModel
    template_name = 'services/service_category_create.html'
    form_class = ServiceCategoryForm
    success_message = "Categoria de serviço criada com sucesso!"

    def get_context_data(self, **kwargs):
        context = super(ServiceCategoryCreateView, self).get_context_data(**kwargs)
        context['business_slug'] = self.kwargs.get('slug')

        return context

    def form_valid(self, model):
        model.instance.business = get_object_or_404(BusinessModel, slug=self.kwargs.get('slug'))
        model.instance.created_by = self.request.user
        model.instance.created = timezone.now()
        return super(ServiceCategoryCreateView, self).form_valid(model)

    def get_success_url(self):
        slug = self.kwargs['slug']
        return reverse_lazy("service_wizard_create", kwargs={'slug': slug,})


class ServiceCategoryDetailView(DetailView):
    model = ServiceCategoryModel
    template_name = 'services/service_category_detail.html'
    slug_url_kwarg = 'service_category_slug'
    #context_object_name = 'service_category'

    def get_context_data(self, **kwargs):
        context = super(ServiceCategoryDetailView, self).get_context_data(**kwargs)
        business = BusinessModel.objects.get(slug=self.kwargs.get('slug'))
        if self.request.user:
            context['user_in'] = self.request.user in business.users.all()
            context['user_id'] = self.request.user.id
        context['business_title'] = business.title
        logo_qrcode = BusinessLogoQrcodeModel.objects.filter(business=business).first()
        if logo_qrcode.logo_img:
            context['logo'] = logo_qrcode.logo_img
        if logo_qrcode.favicon:
            context['favicon'] = logo_qrcode.favicon
        context['service_list'] = get_service_equipment_time_and_price_in_list(business=business, service_category=self.object)
        self.request.session['business_slug'] = business.slug
        self.request.session['logo_qrcode_session_pk'] = logo_qrcode.pk
        self.request.session['service_category_slug'] = self.object.slug
        self.request.session['service_category_title'] = self.object.title
        if 'service_session' in self.request.session:
            del self.request.session['service_session']
        return context


class ServiceViewSet(viewsets.ViewSet):

    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        business = self.kwargs['slug']
        service = ServiceModel.objects.filter(business__slug=business)
        serializer = ServiceSerializer(service, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ServiceModel(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        service = ServiceModel.objects.get(slug=kwargs['service_slug'])
        serializer = ServiceSerializer(instance=service)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        service = ServiceModel.objects.get(slug=kwargs['service_slug'])
        serializer = ServiceSerializer(instance=service, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        service = ServiceModel.objects.get(slug=kwargs['service_slug'])
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(requires_business_owner_or_app_staff, name='dispatch')
class ServiceWizardCreateView(SuccessMessageMixin, SessionWizardView):
    form_list = [ServiceFormOne, ServiceFormTwo]
    template_name = 'services/service_wizard_create.html'
    success_message = "Serviço criado com sucesso!"
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'service_storage'))

    def get_context_data(self, **kwargs):
        context = super(ServiceWizardCreateView, self).get_context_data(**kwargs)
        context['business_slug'] = self.kwargs.get('slug')

        return context

    def done(self, form_list, **kwargs):
        # get merged dictionary from all fields
        form_dict = self.get_all_cleaned_data()
        service = ServiceModel()
        service.business = get_object_or_404(BusinessModel, slug=self.kwargs.get('slug'))
        service.created = timezone.now()
        service.created_by = self.request.user
        for k, v in form_dict.items():
            if k != 'tags':
                setattr(service, k, v)
        service.save()

        self.request.session['service_session'] = True
        price = PriceModel.objects.get(service=service)
        return HttpResponseRedirect(reverse("prices:price_service_update", kwargs={'slug': service.business.slug, 'service_slug': service.slug, 'pk': price.pk}))


class ServiceDetailView(DetailView):
    model = ServiceModel
    template_name = 'services/service_detail.html'
    slug_url_kwarg = 'service_slug'
    #context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super(ServiceDetailView, self).get_context_data(**kwargs)
        business = BusinessModel.objects.get(slug=self.kwargs.get('slug'))
        if self.request.user:
            context['user_in'] = self.request.user in business.users.all()
            context['user_id'] = self.request.user.id
        service_category = ServiceCategoryModel.objects.get(business=business, slug=self.object.service_category.slug)
        context['business_title'] = business.title
        logo_qrcode = BusinessLogoQrcodeModel.objects.filter(business=business).first()
        if logo_qrcode.logo_img:
            context['logo'] = logo_qrcode.logo_img
        if logo_qrcode.favicon:
            context['favicon'] = logo_qrcode.favicon
        context['service_time'] = get_service_equipment_time(self.object)[0][0]
        context['service_equipment_time_list'] = get_service_equipment_time(self.object)[0][1]
        context['service_price'] = PriceModel.objects.filter(service=self.object).first()
        self.request.session['business_slug'] = business.slug
        self.request.session['logo_qrcode_session_pk'] = logo_qrcode.pk
        self.request.session['service_category_slug'] = service_category.slug
        self.request.session['service_category_title'] = service_category.title

        self.request.session['service_slug'] = self.object.slug
        self.request.session['service_title'] = self.object.title

        return context


class EquipmentViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        business = self.kwargs['slug']
        equipment = EquipmentModel.objects.filter(business__slug=business)
        serializer = EquipmentSerializer(equipment, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = EquipmentModel(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        equipment = EquipmentModel.objects.get(slug=kwargs['equipment_slug'])
        serializer = EquipmentSerializer(instance=equipment)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        equipment = EquipmentModel.objects.get(slug=kwargs['equipment_slug'])
        serializer = EquipmentSerializer(instance=equipment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        equipment = EquipmentModel.objects.get(slug=kwargs['equipment_slug'])
        equipment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(requires_business_owner_or_app_staff, name='dispatch')
class EquipmentCreateView(SuccessMessageMixin, CreateView):
    model = EquipmentModel
    template_name = 'services/equipment_create.html'
    form_class = EquipmentForm
    success_message = "Equipamento criado com sucesso!"

    def get_context_data(self, **kwargs):
        context = super(EquipmentCreateView, self).get_context_data(**kwargs)
        context['business_slug'] = self.kwargs.get('slug')

        return context

    def form_valid(self, model):
        model.instance.business = get_object_or_404(BusinessModel, slug=self.kwargs.get('slug'))
        model.instance.created_by = self.request.user
        model.instance.created = timezone.now()
        return super(EquipmentCreateView, self).form_valid(model)

    def get_success_url(self):
        slug = self.kwargs['slug']
        equipment_slug = self.object.slug
        return reverse_lazy("equipment_address_create", kwargs={'slug': slug, 'equipment_slug': equipment_slug})


class EquipmentDetailView(DetailView):
    model = EquipmentModel
    template_name = 'services/equipment_detail.html'
    slug_url_kwarg = 'equipment_slug'
    #context_object_name = 'equipment'

    def get_context_data(self, **kwargs):
        context = super(EquipmentDetailView, self).get_context_data(**kwargs)

        self.request.session['equipment_slug'] = self.object.slug
        self.request.session['equipment_title'] = self.object.title

        return context


class ServiceEquipmentViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        business = self.kwargs['slug']
        service_equipment = ServiceEquipmentModel.objects.filter(service__business__slug=business)
        serializer = ServiceEquipmentSerializer(service_equipment, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ServiceEquipmentModel(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        service_equipment = ServiceEquipmentModel.objects.get(pk=kwargs['pk'])
        serializer = ServiceEquipmentSerializer(instance=service_equipment)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        service_equipment = ServiceEquipmentModel.objects.get(pk=kwargs['pk'])
        serializer = ServiceEquipmentSerializer(instance=service_equipment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        service_equipment = ServiceEquipmentModel.objects.get(pk=kwargs['pk'])
        service_equipment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(requires_business_owner_or_app_staff, name='dispatch')
class ServiceEquipmentCreateView(SuccessMessageMixin, CreateView):
    model = ServiceEquipmentModel
    template_name = 'services/service_equipment_create.html'
    form_class = ServiceEquipmentForm
    success_message = "Equipamento adicionado ao serviço com sucesso!"

    def get_context_data(self, **kwargs):
        context = super(ServiceEquipmentCreateView, self).get_context_data(**kwargs)
        context['business_slug'] = self.kwargs.get('slug')
        service = ServiceModel.objects.get(slug=self.kwargs.get('service_slug'))
        context['service'] = service
        self.request.session['service_slug'] = service.slug
        return context

    def get_form_kwargs(self):
        kwargs = super(ServiceEquipmentCreateView, self).get_form_kwargs()
        business = BusinessModel.objects.filter(slug=self.kwargs.get('slug')).first()
        service = ServiceModel.objects.get(slug=self.kwargs.get('service_slug'))
        kwargs['equipment_replaced'] = get_service_equipment(service)
        kwargs['equipment'] = EquipmentModel.objects.filter(business=business)

        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            business = get_object_or_404(BusinessModel, slug=self.kwargs.get('slug'))
            service = get_object_or_404(ServiceModel, slug=self.kwargs.get('service_slug'))
            form.instance.business = business
            form.instance.service = service
            form.instance.created_by = self.request.user
            form.instance.created = timezone.now()
            return super(ServiceEquipmentCreateView, self).form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("service_equipment_list", kwargs={'slug': self.object.business.slug, 'service_slug': self.object.service.slug})


@method_decorator(requires_business_owner_or_app_staff, name='dispatch')
class ServiceEquipmentDetailView(DetailView):
    model = ServiceEquipmentModel
    template_name = 'services/service_equipment_detail.html'
    pk_url_kwarg = 'pk'
    #context_object_name = 'service_equipment'

    def get_context_data(self, **kwargs):
        context = super(ServiceEquipmentDetailView, self).get_context_data(**kwargs)

        context['service_equipment_time'] = self.object.equipment_time

        return context


@method_decorator(requires_business_owner_or_app_staff, name='dispatch')
class ServiceEquipmentListView(ListView):
    template_name = 'services/service_equipment_list.html'
    model = ServiceEquipmentModel
    context_object_name = 'service_equipment_list'

    def get_queryset(self):
        queryset = super().get_queryset().filter(service__slug=self.kwargs.get('service_slug'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ServiceEquipmentListView, self).get_context_data(**kwargs)
        context['business_slug'] = self.kwargs.get('slug')
        service = ServiceModel.objects.get(slug=self.kwargs.get('service_slug'))
        context['service'] = service
        self.request.session['service_equipment_list_slug'] = service.slug
        if 'service_session' in self.request.session:
            del self.request.session['service_session']
        return context


class EquipmentAddressViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        business = self.kwargs['slug']
        equipment_address = EquipmentAddressModel.objects.filter(address__business__slug=business)
        serializer = EquipmentAddressSerializer(equipment_address, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = EquipmentAddressModel(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        equipment_address = EquipmentAddressModel.objects.get(pk=kwargs['pk'])
        serializer = EquipmentAddressSerializer(instance=equipment_address)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        equipment_address = EquipmentAddressModel.objects.get(pk=kwargs['pk'])
        serializer = EquipmentAddressSerializer(instance=equipment_address, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        equipment_address = EquipmentAddressModel.objects.get(pk=kwargs['pk'])
        equipment_address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(requires_business_owner_or_app_staff, name='dispatch')
class EquipmentAddressCreateView(SuccessMessageMixin, CreateView):
    model = EquipmentAddressModel
    template_name = 'services/equipment_address_create.html'
    form_class = EquipmentAddressForm
    success_message = "Equipamento  adicionado com sucesso!"

    def get_context_data(self, **kwargs):
        context = super(EquipmentAddressCreateView, self).get_context_data(**kwargs)
        context['business_slug'] = self.kwargs.get('slug')
        context['equipment'] = get_object_or_404(EquipmentModel, slug=self.kwargs.get('equipment_slug'))

        return context

    def get_form_kwargs(self):
        kwargs = super(EquipmentAddressCreateView, self).get_form_kwargs()
        business = BusinessModel.objects.filter(slug=self.kwargs.get('slug')).first()
        business_address_list = BusinessAddressModel.objects.filter(business=business)
        kwargs['address'] = [[x.id, x] for x in business_address_list]

        return kwargs

    def form_valid(self, form):
        equipment = get_object_or_404(EquipmentModel, slug=self.kwargs.get('equipment_slug'))
        instance = form.save(commit=False)
        instance.equipment = equipment
        instance.created_by = self.request.user
        instance.created = timezone.now()
        return super(EquipmentAddressCreateView, self).form_valid(form)

    def get_success_url(self):
        slug = self.kwargs['slug']
        equipment_slug = self.kwargs['equipment_slug']
        if 'service_slug' in self.request.session:
            service_slug = self.request.session['service_slug']
            return reverse_lazy("service_equipment_create", kwargs={'slug': slug, 'service_slug': service_slug})
        else:
            return reverse_lazy("equipment_detail", kwargs={'slug': slug, 'equipment_slug': equipment_slug})


class EquipmentAddressDetailView(DetailView):
    model = EquipmentAddressModel
    template_name = 'services/equipment_address_detail.html'
    pk_url_kwarg = 'pk'
    #context_object_name = 'equipment_address'

    def get_context_data(self, **kwargs):
        context = super(EquipmentAddressDetailView, self).get_context_data(**kwargs)

        context['equipment_address'] = self.object.address

        return context

