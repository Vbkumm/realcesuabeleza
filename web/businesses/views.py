from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.views.generic import ListView, DetailView, DeleteView, UpdateView

from .models import (BusinessModel,
                     BusinessAddressModel,
                     BusinessPhoneModel)
from .serializers import (BusinessSerializer,
                          BusinessAddressSerializer,
                          BusinessPhoneSerializer)


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

        self.request.session['business_slug'] = self.object.slug
        self.request.session['business_title'] = self.object.title
        self.request.session['business_logo'] = self.object.logo_url

        return context


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


