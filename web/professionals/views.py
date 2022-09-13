import os
from rest_framework import viewsets, status
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, CreateView, DetailView
from django.urls import reverse_lazy, reverse
from formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.utils import timezone
from django.contrib.messages.views import SuccessMessageMixin
from rest_framework.response import Response
from lib.templatetags.permissions import requires_business_owner_or_app_staff
from businesses.models import BusinessModel
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
                     CloseScheduleModel)
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
    form_list = [ProfessionalFormOne, ProfessionalFormTwo]
    template_name = 'professionals/professional_wizard_create.html'
    success_message = "Serviço criado com sucesso!"
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'professional_storage'))

    def get_context_data(self, **kwargs):
        context = super(ProfessionalWizardCreateView, self).get_context_data(**kwargs)
        context['business_slug'] = self.kwargs.get('slug')
        self.request.session['professional_create_session'] = True
        return context

    def done(self, form_list, **kwargs):
        # get merged dictionary from all fields
        form_dict = self.get_all_cleaned_data()
        professional = ProfessionalModel()
        professional.business = get_object_or_404(BusinessModel, slug=self.kwargs.get('slug'))
        professional.created = timezone.now()
        professional.created_by = self.request.user
        for k, v in form_dict.items():
            if k != 'tags':
                setattr(professional, k, v)
        professional.save()

        return HttpResponseRedirect(reverse("professionals:professional_detail", kwargs={'slug': professional.business.slug, 'professional_slug': professional.slug}))


class ProfessionalDetailView(DetailView):
    model = ProfessionalModel
    template_name = 'professionals/professional_detail.html'
    slug_url_kwarg = 'professional_slug'
    #context_object_name = 'professional'

    def get_context_data(self, **kwargs):
        context = super(ProfessionalDetailView, self).get_context_data(**kwargs)

        self.request.session['professional_slug'] = self.object.slug
        self.request.session['professional_name'] = self.object.name

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

        return context

    def form_valid(self, model):
        model.instance.business = get_object_or_404(BusinessModel, slug=self.kwargs.get('slug'))
        model.instance.created_by = self.request.user
        model.instance.created = timezone.now()
        return super().form_valid(model)

    def get_success_url(self):
        business_slug = self.kwargs.get('slug')
        if 'professional_create_session' in self.request.session:
            return reverse_lazy('professional_wizard_create', kwargs={'slug': business_slug,})
        else:
            return reverse_lazy('professional_category_detail', kwargs={'slug': business_slug, 'professional_category_slug': self.object.slug})


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