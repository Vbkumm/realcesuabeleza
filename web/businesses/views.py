import os
from django.http import JsonResponse
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
from lib.templatetags.permissions import requires_business_owner_or_app_staff, IsBusinesssOwnerOrStaff
from .models import (BusinessModel,
                     BusinessAddressModel,
                     BusinessPhoneModel,
                     BusinessLogoQrcodeModel,
                     get_phones_by_addresses_by_business)
from .forms import (BusinessUserInnForm,
                    BusinessCreateForm1,
                    BusinessCreateForm2,
                    BusinessCreateForm3,
                    BusinessAddressForm1,
                    BusinessAddressForm2,
                    BusinessAddressForm3,
                    BusinessPhoneForm,
                    BusinessLogoQrcodeForm,)
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
        if 'business_name' in self.request.session:
            del self.request.session['business_name']
        if 'business_email' in self.request.session:
            del self.request.session['business_email']
        if 'business_federal_id' in self.request.session:
            del self.request.session['business_federal_id']
        if 'zip_code' in self.request.session:
            del self.request.session['zip_code']
        if 'street' in self.request.session:
            del self.request.session['street']
        if 'street_number' in self.request.session:
            del self.request.session['street_number']
        if 'district' in self.request.session:
            del self.request.session['district']
        if 'city' in self.request.session:
            del self.request.session['city']
        if 'state' in self.request.session:
            del self.request.session['state']
        if self.request.user:
            context['user_in'] = self.request.user in self.object.users.all()
            context['user_id'] = self.request.user.id
        logo_qrcode = BusinessLogoQrcodeModel.objects.filter(business=self.object).first()
        if logo_qrcode:
            context['qr_code'] = logo_qrcode.qrcode_img
            print(logo_qrcode)
            if logo_qrcode.logo_rgb_color:
                bg_color = rgb_color_generator(logo_qrcode.logo_rgb_color).split(",")
                context['bg_color'] = bg_color
                self.request.session['text_color'] = bg_color[1]
                self.request.session['background_color'] = bg_color[0]
                nav_color = 'light'
                if bg_color[1] == 'light':
                    nav_color = 'dark'
                self.request.session['nav_color'] = nav_color
            if logo_qrcode.logo_img:
                context['logo'] = logo_qrcode.logo_img
            if logo_qrcode.favicon:
                context['favicon'] = logo_qrcode.favicon
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


@method_decorator(requires_business_owner_or_app_staff, name='dispatch')
class BusinessLogoQrcodeCreateView(SuccessMessageMixin, CreateView):

    def get(self, request, *args, **kwargs):
        business = get_object_or_404(BusinessModel, slug=self.kwargs.get('slug'))
        is_owner = False
        if self.request.user in business.owners.all():
            is_owner = True
        logo_qrcode = BusinessLogoQrcodeModel.objects.filter(business=business).first()

        return render(self.request, 'businesses/business_logo_qrcode_create.html', {'slug': business.slug,
                                                                                    'business_logo_qrcode': logo_qrcode,
                                                                                    'is_owner': is_owner,
                                                                                    'title': business.title,})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(business__owners__in=self.request.user)

    def post(self, request, *args, **kwargs):
        business = get_object_or_404(BusinessModel, sulg=self.kwargs.get('slug'))
        if request.method == 'POST':
            form = BusinessLogoQrcodeForm(self.request.POST, self.request.FILES)

            if form.is_valid():

                logo_img = form.save(commit=False)
                logo_img.business = business
                logo_img.updated_by = self.request.user
                logo_img.updated_at = timezone.now()
                logo_img.save()
                data = {'is_valid': True,
                        'name': logo_img.logo_img.name.replace("img/businesses_logo/", ""),
                        'url': logo_img.logo_img.url,
                        }
                print('veio aqui')

            else:
                data = {'is_valid': False}

            return JsonResponse(data)


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


#acrecentar mixiowner
class BusinessAddressWizardCreateView(IsBusinesssOwnerOrStaff, LoginRequiredMixin, SuccessMessageMixin, SessionWizardView):
    form_list = [BusinessAddressForm1, BusinessAddressForm2, BusinessAddressForm3]
    template_name = 'businesses/business_address_wizard_create.html'
    success_message = "Salão criado com sucesso!"
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'business_address_storage'))

    def get_context_data(self, **kwargs):
        context = super(BusinessAddressWizardCreateView, self).get_context_data(**kwargs)
        if 'zip_code' in self.request.session:
            del self.request.session['zip_code']
        if 'street' in self.request.session:
            del self.request.session['street']
        if 'street_number' in self.request.session:
            del self.request.session['street_number']
        if 'district' in self.request.session:
            del self.request.session['district']
        if 'city' in self.request.session:
            del self.request.session['city']
        if 'state' in self.request.session:
            del self.request.session['state']

        business_slug = get_object_or_404(BusinessModel, slug=self.kwargs.get('slug'))
        context['business_slug'] = business_slug

        return context

    def get_form_kwargs(self, step=None):
        kwargs = super(BusinessAddressWizardCreateView, self).get_form_kwargs(step)

        if step == '1':
            zip_code = self.get_cleaned_data_for_step('0')['zip_code']
            street = self.get_cleaned_data_for_step('0')['street']
            self.request.session['street'] = street
            self.request.session['zip_code'] = zip_code

        if step == '2':
            street_number = self.get_cleaned_data_for_step('1')['street_number']
            self.request.session['street_number'] = street_number
            district = self.get_cleaned_data_for_step('0')['district']
            city = self.get_cleaned_data_for_step('0')['city']
            state = self.get_cleaned_data_for_step('0')['state']
            kwargs.update({'district': district,
                           'city': city,
                           'state': state,
                           })

        return kwargs

    def done(self, form_list, **kwargs):
        # get merged dictionary from all fields
        form_dict = self.get_all_cleaned_data()
        business_address = BusinessAddressModel()
        business_address.business = get_object_or_404(BusinessModel, slug=self.kwargs.get('slug'))
        business_address.created_by = self.request.user
        business_address.created = timezone.now()
        for k, v in form_dict.items():
            if k != 'tags':
                setattr(business_address, k, v)
        business_address.save()

        return HttpResponseRedirect(reverse("business_phone_create", kwargs={'slug': business_address.business.slug, 'pk': business_address.pk}))


@method_decorator(requires_business_owner_or_app_staff, name='dispatch')
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


@method_decorator(requires_business_owner_or_app_staff, name='dispatch')
class BusinessPhoneCreateView(SuccessMessageMixin, CreateView):
    model = BusinessPhoneModel
    template_name = 'businesses/business_phone_create.html'
    form_class = BusinessPhoneForm
    pk_url_kwarg = 'pk'
    success_message = "Telefone adicionado com sucesso!"

    def get_context_data(self, **kwargs):
        context = super(BusinessPhoneCreateView, self).get_context_data(**kwargs)
        business = get_object_or_404(BusinessModel, slug=self.kwargs.get('slug'))
        context['business_slug'] = business
        return context

    def form_valid(self, model):

        model.instance.business = get_object_or_404(BusinessModel, slug=self.kwargs.get('slug'))
        model.instance.address = get_object_or_404(BusinessAddressModel, pk=self.kwargs.get('pk'))
        model.instance.created_by = self.request.user
        model.instance.created = timezone.now()
        return super(BusinessPhoneCreateView, self).form_valid(model)

    def get_success_url(self):
        business = get_object_or_404(BusinessModel, slug=self.kwargs.get('slug'))
        return reverse_lazy('business_detail', kwargs={'slug': business.slug})
