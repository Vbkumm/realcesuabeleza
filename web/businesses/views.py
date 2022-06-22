import os
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, Http404, get_object_or_404
from django.urls import reverse_lazy, reverse
from formtools.wizard.views import SessionWizardView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage
from rest_framework import viewsets, status
from rest_framework.response import Response
from realcesuabeleza import settings
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from lib.templatetags.permissions import requires_business_owner_or_app_staff
from .models import (BusinessModel,
                     BusinessAddressModel,
                     BusinessPhoneModel,
                     get_phones_by_addresses_by_business)
from .forms import (BusinessUserInnForm,
                    BusinessCreateForm1,
                    BusinessCreateForm2,
                    BusinessCreateForm3,
                    BusinessAddressForm,)
from .utils import rgb_color_generator
from .serializers import (BusinessSerializer,
                          BusinessAddressSerializer,
                          BusinessPhoneSerializer)
from services.models import get_categories_by_business
from professionals.models import get_professionals_by_business


class BusinessViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        businesses = BusinessModel.objects.all()
        serializer = BusinessSerializer(businesses, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = BusinessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        business = BusinessModel.objects.get(slug=kwargs['slug'])
        serializer = BusinessSerializer(instance=business)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        business = BusinessModel.objects.get(slug=kwargs['slug'])
        serializer = BusinessSerializer(instance=business, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        business = BusinessModel.objects.get(slug=kwargs['slug'])
        business.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BusinessDetailView(DetailView):
    model = BusinessModel
    template_name = 'businesses/business_detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'business'

    def get_context_data(self, **kwargs):
        context = super(BusinessDetailView, self).get_context_data(**kwargs)

        if self.request.user:
            context['user_in'] = self.request.user in self.object.users.all()
            context['user_id'] = self.request.user.id
        if self.object.logo_rgb_color:
            bg_color = rgb_color_generator(self.object.logo_rgb_color).split(",")
            context['bg_color'] = bg_color
            self.request.session['text_color'] = bg_color[1]
            self.request.session['background_color'] = bg_color[0]
            nav_color = 'light'
            if bg_color[1] == 'light':
                nav_color = 'dark'
            self.request.session['nav_color'] = nav_color
        context['services_categories'] = get_categories_by_business(business=self.object)
        context['professional_list'] = get_professionals_by_business(business=self.object)
        context['phone_and_address_list'] = get_phones_by_addresses_by_business(business=self.object)
        self.request.session['business_slug'] = self.object.slug
        self.request.session['business_title'] = self.object.title

        return context


class BusinessWizardCreateView(LoginRequiredMixin, SuccessMessageMixin, SessionWizardView):
    form_list = [BusinessCreateForm1, BusinessCreateForm2, BusinessCreateForm3]
    template_name = 'businesses/business_wizard_create.html'
    success_message = "Salão criado com sucesso!"
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'business_storage'))

    def get_context_data(self, **kwargs):
        context = super(BusinessWizardCreateView, self).get_context_data(**kwargs)
        if 'business_name' in self.request.session:
            business_name = self.request.session['business_name']
            del self.request.session['business_name']
            context['business_name'] = business_name
        if 'business_email' in self.request.session:
            business_name = self.request.session['business_email']
            del self.request.session['business_email']
            context['business_email'] = business_name
        if 'business_federal_id' in self.request.session:
            business_federal_id = self.request.session['business_federal_id']
            del self.request.session['business_federal_id']
            context['business_federal_id'] = business_federal_id

        return context

    def get_form_kwargs(self, step=None):
        kwargs = super(BusinessWizardCreateView, self).get_form_kwargs(step)

        if step == '1':
            business_name = self.get_cleaned_data_for_step('0')['title']
            self.request.session['business_name'] = business_name

        if step == '2':
            business_email = self.get_cleaned_data_for_step('1')['email']
            self.request.session['business_email'] = business_email
            business_federal_id = self.get_cleaned_data_for_step('1')['federal_id']
            self.request.session['business_federal_id'] = business_federal_id

        return kwargs

    def done(self, form_list, **kwargs):
        # get merged dictionary from all fields
        form_dict = self.get_all_cleaned_data()
        business = BusinessModel()
        business.created_by = self.request.user
        business.created = timezone.now()
        for k, v in form_dict.items():
            if k != 'tags':
                setattr(business, k, v)
        business.save()
        business.owners.add(self.request.user)
        business.users.add(self.request.user)
        business.save()

        return HttpResponseRedirect(reverse("business_address_create", kwargs={'slug': business.slug}))


@login_required
def user_business_add(request, slug):
    business = get_object_or_404(BusinessModel, slug=slug)
    business_user_inn_form = BusinessUserInnForm(request.POST or None)
    if request.method == 'GET':
        return HttpResponseRedirect((reverse_lazy("business_detail",  kwargs={'slug': business.slug})))
    else:
        if request.method == 'POST' and business_user_inn_form.is_valid():
            business.users.add(business_user_inn_form.cleaned_data['users'])
            business.save()
            return HttpResponseRedirect(reverse_lazy("business_detail",  kwargs={'slug': business.slug}))
        raise Http404()


class BusinessAddressViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        business_address = BusinessAddressModel.objects.All()
        serializer = BusinessAddressSerializer(business_address, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = BusinessAddressModel(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        business_address = BusinessAddressModel.objects.get(id=kwargs['pk'])
        serializer = BusinessAddressSerializer(instance=business_address)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        business_address = BusinessAddressModel.objects.get(id=kwargs['pk'])
        serializer = BusinessAddressSerializer(instance=business_address, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        business_address = BusinessAddressModel.objects.get(id=kwargs['pk'])
        business_address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BusinessAddressDetailView(DetailView):
    model = BusinessModel
    template_name = 'businesses/business_address_detail.html'
    pk_url_kwarg = 'pk'
    #context_object_name = 'business_address'


@method_decorator(requires_business_owner_or_app_staff, name='dispatch')
class BusinessAddressCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = BusinessAddressModel
    template_name = 'businesses/business_address_create.html'
    form_class = BusinessAddressForm
    pk_url_kwarg = 'pk'
    success_message = "Endereço adicionado com sucesso!"

    def get_context_data(self, **kwargs):
        context = super(BusinessAddressCreateView, self).get_context_data(**kwargs)
        business_slug = get_object_or_404(BusinessModel, slug=self.kwargs.get('slug'))
        context['business_slug'] = business_slug
        return context

    def form_valid(self, model):
        model.instance.business = get_object_or_404(BusinessModel, slug=self.kwargs.get('slug'))
        model.instance.created_by = self.request.user
        model.instance.created = timezone.now()
        return super(BusinessAddressCreateView, self).form_valid(model)

    def get_success_url(self):
        business = get_object_or_404(BusinessModel, slug=self.kwargs.get('slug'))
        return reverse_lazy('business_detail', kwargs={'slug': business.slug})


class BusinessPhoneViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        business_phone = BusinessPhoneModel.objects.All()
        serializer = BusinessPhoneSerializer(business_phone, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = BusinessPhoneModel(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        business_phone = BusinessPhoneModel.objects.get(id=kwargs['pk'])
        serializer = BusinessPhoneSerializer(instance=business_phone)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        business_phone = BusinessPhoneModel.objects.get(id=kwargs['pk'])
        serializer = BusinessPhoneSerializer(instance=business_phone, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        business_phone = BusinessPhoneModel.objects.get(id=kwargs['pk'])
        business_phone.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


