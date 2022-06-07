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
from django.views.generic import ListView, DetailView, DeleteView, UpdateView

from .models import (BusinessModel,
                     BusinessAddressModel,
                     BusinessPhoneModel,
                     get_phones_by_addresses_by_business)
from .forms import (BusinessUserInnForm,
                    BusinessCreateForm1,
                    BusinessCreateForm2,)
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
        string = self.object.logo_rgb_color
        if self.request.user:
            context['user_in'] = self.request.user in self.object.users.all()
            context['user_id'] = self.request.user.id
        bg_color = rgb_color_generator(string).split(",")
        context['bg_color'] = bg_color
        context['services_categories'] = get_categories_by_business(business=self.object)
        context['professional_list'] = get_professionals_by_business(business=self.object)
        context['phone_and_address_list'] = get_phones_by_addresses_by_business(business=self.object)
        self.request.session['business_slug'] = self.object.slug
        self.request.session['business_title'] = self.object.title
        self.request.session['text_color'] = bg_color[1]
        self.request.session['bg_color'] = bg_color[0]

        return context


class BusinessWizardCreateView(LoginRequiredMixin, SuccessMessageMixin, SessionWizardView):
    form_list = [BusinessCreateForm1, BusinessCreateForm1,]
    template_name = 'businesses/business_wizard_create.html'
    success_message = "Salão criado com sucesso!"
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'business_storage'))

    def done(self, form_list, **kwargs):
        # get merged dictionary from all fields
        form_dict = self.get_all_cleaned_data()
        business = BusinessModel()
        business.created_by = self.request.user
        business.owners.add(self.request.user)
        business.created = timezone.now()
        for k, v in form_dict.items():
            if k != 'tags':
                setattr(business, k, v)
        business.save()

        return HttpResponseRedirect(reverse("business_detail", kwargs={'slug': business.slug}))


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


