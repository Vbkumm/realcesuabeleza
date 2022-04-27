from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import (BusinessModel,
                     BusinessAddressModel,
                     BusinessPhoneModel)
from .serializers import (BusinessSerializer,
                          BusinessAddressSerializer,
                          BusinessPhoneSerializer)


class BusinessViewSet(viewsets.ViewSet):

    def list(self, request):
        businesses = BusinessModel.objects.All()
        serializer = BusinessSerializer(businesses, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = BusinessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        business = BusinessModel.objects.get(id=pk)
        serializer = BusinessSerializer(business)
        return Response(serializer.data)

    def update(self, request, pk=None):
        business = BusinessModel.objects.get(id=pk)
        serializer = BusinessSerializer(instance=business, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        business = BusinessModel.objects.get(id=pk)
        business.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


