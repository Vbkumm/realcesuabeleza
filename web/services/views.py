from rest_framework import viewsets, status
from rest_framework.response import Response
from django.views.generic import ListView, DetailView, DeleteView, UpdateView

from .models import (ServiceCategoryModel,
                     ServiceModel,
                     EquipmentModel,
                     ServiceEquipmentModel,
                     EquipmentAddressModel,
                     )
from .serializers import (ServiceCategorySerializer,
                          ServiceSerializer,
                          EquipmentSerializer,
                          ServiceEquipmentSerializer,
                          EquipmentAddressSerializer,)


class ServiceCategoryViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        service_category = ServiceCategoryModel.objects.all()
        serializer = ServiceCategorySerializer(service_category, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ServiceCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        service_category = ServiceCategoryModel.objects.get(slug=kwargs['slug'])
        serializer = ServiceCategorySerializer(instance=service_category)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        service_category = ServiceCategoryModel.objects.get(slug=kwargs['slug'])
        serializer = ServiceCategorySerializer(instance=service_category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        service_category = ServiceCategoryModel.objects.get(slug=kwargs['slug'])
        service_category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ServiceCategoryDetailView(DetailView):
    model = ServiceCategoryModel
    template_name = 'services/service_category_detail.html'
    slug_url_kwarg = 'service_category_slug'
    context_object_name = 'service_category'

    def get_context_data(self, **kwargs):
        context = super(ServiceCategoryDetailView, self).get_context_data(**kwargs)

        self.request.session['service_category_slug'] = self.object.slug
        self.request.session['service_category_title'] = self.object.title

        return context


class ServiceViewSet(viewsets.ViewSet):

    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        service = ServiceModel.objects.all()
        serializer = ServiceSerializer(service, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ServiceModel(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        service = ServiceModel.objects.get(slug=kwargs['slug'])
        serializer = ServiceSerializer(instance=service)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        service = ServiceModel.objects.get(slug=kwargs['slug'])
        serializer = ServiceSerializer(instance=service, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        service = ServiceModel.objects.get(slug=kwargs['slug'])
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ServiceDetailView(DetailView):
    model = ServiceModel
    template_name = 'services/service_detail.html'
    slug_url_kwarg = 'service_slug'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super(ServiceDetailView, self).get_context_data(**kwargs)

        self.request.session['service_slug'] = self.object.slug
        self.request.session['service_title'] = self.object.title

        return context


class EquipmentViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        equipment = EquipmentModel.objects.all()
        serializer = EquipmentSerializer(equipment, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = EquipmentModel(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        equipment = EquipmentModel.objects.get(slug=kwargs['slug'])
        serializer = EquipmentSerializer(instance=equipment)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        equipment = EquipmentModel.objects.get(slug=kwargs['slug'])
        serializer = EquipmentSerializer(instance=equipment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        equipment = EquipmentModel.objects.get(slug=kwargs['slug'])
        equipment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EquipmentDetailView(DetailView):
    model = EquipmentModel
    template_name = 'services/equipment_detail.html'
    slug_url_kwarg = 'equipment_slug'
    context_object_name = 'equipment'

    def get_context_data(self, **kwargs):
        context = super(EquipmentDetailView, self).get_context_data(**kwargs)

        self.request.session['equipment_slug'] = self.object.slug
        self.request.session['equipment_title'] = self.object.title

        return context