from rest_framework import viewsets, status
from rest_framework.response import Response
from django.views.generic import ListView, DetailView, DeleteView, UpdateView

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