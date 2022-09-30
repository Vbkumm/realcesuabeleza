import os
from rest_framework import viewsets, status
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, CreateView, DetailView
from django.urls import reverse_lazy, reverse
from formtools.wizard.views import SessionWizardView
from django.conf import settings
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.utils import timezone
from django.contrib.messages.views import SuccessMessageMixin
from rest_framework.response import Response
from lib.templatetags.permissions import requires_business_owner_or_app_staff, flush_session
from businesses.models import BusinessModel, BusinessLogoQrcodeModel
from businesses.utils import rgb_color_generator
from services.models import ServiceCategoryModel
from .models import (ProfessionalUserModel,
                     ProfessionalModel,
                     ProfessionalServiceCategoryModel,
                     ProfessionalCategoryModel,
                     ProfessionalPhoneModel,
                     ProfessionalAddressModel,
                     ProfessionalScheduleModel,
                     ProfessionalExtraSkillModel,
                     ProfessionalNoSkillModel,
                     OpenScheduleModel,
                     CloseScheduleModel,
                     get_services_by_service_category)
from .serializers import (ProfessionalUserSerializer,
                          ProfessionalSerializer,
                          ProfessionalServiceCategorySerializer,
                          ProfessionalCategorySerializer,
                          ProfessionalPhoneSerializer,
                          ProfessionalAddressSerializer,
                          ProfessionalScheduleSerializer,
                          ProfessionalExtraSkillSerializer,
                          ProfessionalNoSkillSerializer,
                          OpenScheduleSerializer,
                          CloseScheduleSerializer,)
from .forms import (ProfessionalCategoryForm,
                    ProfessionalFormOne,
                    ProfessionalFormTwo,
                    ProfessionalFormTree,
                    ProfessionalFormFour,
                    ProfessionalSelectCategoryForm,
                    ProfessionalCategoryUpdateServicesCategoryForm,
                    )


class ProfessionalViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        business = self.kwargs['slug']
        professional = ProfessionalModel.objects.filter(business__slug=business)
        serializer = ProfessionalSerializer(professional, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ProfessionalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        professional = ProfessionalModel.objects.get(slug=kwargs['professional_slug'])
        serializer = ProfessionalSerializer(instance=professional)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        professional = ProfessionalModel.objects.get(slug=kwargs['professional_slug'])
        serializer = ProfessionalSerializer(instance=professional, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        professional = ProfessionalModel.objects.get(slug=kwargs['professional_slug'])
        professional.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(requires_business_owner_or_app_staff, name='dispatch')
class ProfessionalWizardCreateView(SuccessMessageMixin, SessionWizardView):
    form_list = [ProfessionalFormOne, ProfessionalFormTwo, ProfessionalFormTree, ProfessionalFormFour]
    template_name = 'professionals/professional_wizard_create.html'
    success_message = "Serviço criado com sucesso!"
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'professional_storage'))

    def get_context_data(self, **kwargs):
        context = super(ProfessionalWizardCreateView, self).get_context_data(**kwargs)
        context['business_slug'] = self.kwargs.get('slug')
        self.request.session['professional_create_session'] = True
        return context

    def get_form_kwargs(self, step=None):
        kwargs = super(ProfessionalWizardCreateView, self).get_form_kwargs(step)
        if step == '1':
            professional_name = self.get_cleaned_data_for_step('0')['title']
            self.request.session['professional_name'] = professional_name
        if step == '2':
            professional_birth_date = self.get_cleaned_data_for_step('1')['birth_date']
            self.request.session['professional_birth_date'] = str(datetime.strftime(professional_birth_date, "%d-%m-%Y"))
        if step == '3':
            professional_began_date = self.get_cleaned_data_for_step('2')['began_date']
            self.request.session['professional_began_date'] = str(datetime.strftime(professional_began_date, "%d-%m-%Y"))

        return kwargs

    def done(self, form_list, **kwargs):
        # get merged dictionary from all fields
        form_dict = self.get_all_cleaned_data()
        professional = ProfessionalModel()
        business = get_object_or_404(BusinessModel, slug=self.kwargs.get('slug'))
        professional.business = business
        professional.created = timezone.now()
        professional.created_by = self.request.user
        for k, v in form_dict.items():
            if k != 'tags':
                setattr(professional, k, v)

        professional.save()

        return HttpResponseRedirect(reverse("professional_select_category_update", kwargs={'slug': business.slug, 'professional_slug': professional.slug}))


@method_decorator(requires_business_owner_or_app_staff, name='dispatch')
class ProfessionalSelectCategoryUpdateView(SuccessMessageMixin, UpdateView):

    form_class = ProfessionalSelectCategoryForm
    model = ProfessionalModel
    #context_object_name = 'professional'
    slug_url_kwarg = 'professional_slug'
    template_name = 'professionals/professional_select_category_update.html'
    success_message = "Alterações realizadas com sucesso!"

    def get_context_data(self, **kwargs):

        context = super(ProfessionalSelectCategoryUpdateView, self).get_context_data(**kwargs)
        context['business_slug'] = self.kwargs.get('slug')
        professional = ProfessionalModel.objects.get(slug=self.kwargs.get('professional_slug'))
        context['professional'] = professional
        self.request.session['professional_slug'] = professional.slug
        if "professional_create_session" in self.request.session:
            self.request.session['professional_create_session'] = True
            context['professional_slug'] = professional.slug
        return context

    def get_form_kwargs(self):
        kwargs = super(ProfessionalSelectCategoryUpdateView, self).get_form_kwargs()
        business = get_object_or_404(BusinessModel, slug=self.kwargs.get('slug'))
        kwargs['categories'] = ProfessionalCategoryModel.objects.filter(business=business, is_active=True,)
        return kwargs

    def form_valid(self, form):

        form.instance.updated_at = timezone.now()
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        business = self.kwargs.get('slug')
        professional = self.kwargs.get('professional_slug')

        return reverse_lazy("professional_detail", kwargs={'slug': business, 'professional_slug': professional})


class ProfessionalDetailView(DetailView):
    model = ProfessionalModel
    template_name = 'professionals/professional_detail.html'
    slug_url_kwarg = 'professional_slug'
    #context_object_name = 'professional'

    def get_context_data(self, **kwargs):
        context = super(ProfessionalDetailView, self).get_context_data(**kwargs)
        flush_session(self.request)
        business = BusinessModel.objects.get(slug=self.kwargs.get('slug'))
        if self.request.user:
            context['user_in'] = self.request.user in business.users.all()
            context['user_id'] = self.request.user.id
            if self.request.user in business.owners.all():
                context['is_owner'] = True
        context['business_title'] = business.title
        logo_qrcode = BusinessLogoQrcodeModel.objects.filter(business=business).first()
        if logo_qrcode:
            context['qr_code'] = logo_qrcode.qrcode_img
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
        professional_category_list = self.object.categories.all()
        context['professional_category_list'] = professional_category_list
        context['professional_service_list'] = get_services_by_service_category(professional_category_list)
        self.request.session['business_slug'] = business.slug
        self.request.session['logo_qrcode_session_pk'] = logo_qrcode.pk
        self.request.session['professional_slug'] = self.object.slug
        self.request.session['professional_name'] = self.object.title

        return context


class ProfessionalCategoryViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        business = self.kwargs['slug']
        professional_category = ProfessionalCategoryModel.objects.filter(business__slug=business)
        serializer = ProfessionalCategorySerializer(professional_category, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ProfessionalCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        professional_category = ProfessionalCategoryModel.objects.get(slug=kwargs['professional_category_slug'])
        serializer = ProfessionalCategorySerializer(instance=professional_category)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        professional_category = ProfessionalCategoryModel.objects.get(slug=kwargs['professional_category_slug'])
        serializer = ProfessionalCategorySerializer(instance=professional_category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        professional_category = ProfessionalCategoryModel.objects.get(slug=kwargs['professional_category_slug'])
        professional_category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(requires_business_owner_or_app_staff, name='dispatch')
class ProfessionalCategoryCreateView(SuccessMessageMixin, CreateView):
    model = ProfessionalCategoryModel
    template_name = 'professionals/professional_category_create.html'
    form_class = ProfessionalCategoryForm
    success_message = "Categoria de profissional criada com sucesso!"

    def get_context_data(self, **kwargs):
        context = super(ProfessionalCategoryCreateView, self).get_context_data(**kwargs)
        context['business_slug'] = self.kwargs.get('slug')
        if "professional_create_session" in self.request.session:
            self.request.session['professional_create_session'] = True
        if "professional_slug" in self.request.session:
            context['professional_slug'] = self.request.session['professional_slug']

        return context

    def form_valid(self, model):
        model.instance.business = get_object_or_404(BusinessModel, slug=self.kwargs.get('slug'))
        model.instance.created_by = self.request.user
        model.instance.created = timezone.now()
        return super().form_valid(model)

    def get_success_url(self):
        business_slug = self.kwargs.get('slug')
        if 'professional_create_session' and 'professional_slug' in self.request.session:
            return reverse_lazy('professional_category_set_services_category', kwargs={'slug': business_slug, 'professional_category_slug': self.object.slug})
        else:
            return reverse_lazy('professional_category_detail', kwargs={'slug': business_slug, 'professional_category_slug': self.object.slug})


@method_decorator(requires_business_owner_or_app_staff, name='dispatch')
class ProfessionalCategorySetServicesCategoryView(SuccessMessageMixin, CreateView):
    model = ProfessionalServiceCategoryModel
    form_class = ProfessionalCategoryUpdateServicesCategoryForm
    template_name = 'professionals/professional_category_set_services_category.html'

    def get_context_data(self, **kwargs):
        context = super(ProfessionalCategorySetServicesCategoryView, self).get_context_data(**kwargs)
        context['business_slug'] = self.kwargs.get('slug')
        if "professional_create_session" in self.request.session:
            self.request.session['professional_create_session'] = True
        if "professional_slug" in self.request.session:
            context['professional_slug'] = self.request.session['professional_slug']
        context['professional_category_slug'] = self.kwargs.get('professional_category_slug')
        context['professional_category'] = ProfessionalCategoryModel.objects.get(slug=self.kwargs.get('professional_category_slug'))
        return context

    def get_form_kwargs(self):

        kwargs = super(ProfessionalCategorySetServicesCategoryView, self).get_form_kwargs()
        business = get_object_or_404(BusinessModel, slug=self.kwargs.get('slug'))
        kwargs['service_category'] = ServiceCategoryModel.objects.filter(business=business, is_active=True,)
        return kwargs

    def form_valid(self, model):
        model.instance.business = get_object_or_404(BusinessModel, slug=self.kwargs.get('slug'))
        model.instance.professional_category = get_object_or_404(ProfessionalCategoryModel, slug=self.kwargs.get('professional_category_slug'))
        model.instance.created_by = self.request.user
        model.instance.created = timezone.now()
        return super().form_valid(model)

    def get_success_url(self):
        business_slug = self.kwargs.get('slug')
        if 'professional_create_session' and 'professional_slug' in self.request.session:
            return reverse_lazy('professional_select_category_update', kwargs={'slug': business_slug, 'professional_slug': self.request.session['professional_slug']})
        else:
            return reverse_lazy('professional_category_detail', kwargs={'slug': business_slug, 'professional_category_slug': self.kwargs.get('professional_category_slug')})


class ProfessionalCategoryDetailView(DetailView):
    model = ProfessionalCategoryModel
    template_name = 'professionals/professional_category_detail.html'
    slug_url_kwarg = 'professional_category_slug'
    #context_object_name = 'professional'

    def get_context_data(self, **kwargs):
        context = super(ProfessionalCategoryDetailView, self).get_context_data(**kwargs)

        self.request.session['professional_category_slug'] = self.object.slug
        self.request.session['professional_category_name'] = self.object.title

        return context