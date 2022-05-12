from rest_framework import viewsets, status
from rest_framework.response import Response
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from .models import (CustomerModel,
                     CustomerUserModel,
                     CustomerAddressModel,
                     CustomerPhoneModel,)
from .serializers import (CustomerSerializer,
                          CustomerPhoneSerializer,
                          CustomerUserSerializer,
                          CustomerAddressSerializer)


class CustomerViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        business = self.kwargs['slug']
        customer = CustomerModel.objects.filter(business__slug=business)
        serializer = CustomerSerializer(customer, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        customer = CustomerModel.objects.get(pk=kwargs['pk'])
        serializer = CustomerSerializer(instance=customer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        customer = CustomerModel.objects.get(pk=kwargs['pk'])
        serializer = CustomerSerializer(instance=customer, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        customer = CustomerModel.objects.get(pk=kwargs['pk'])
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomerDetailView(DetailView):
    model = CustomerModel
    template_name = 'customers/customer_detail.html'
    pk_url_kwarg = 'pk'
    #context_object_name = 'customer'

    def get_context_data(self, **kwargs):
        context = super(CustomerDetailView, self).get_context_data(**kwargs)

        self.request.session['customer_email'] = self.object.email
        self.request.session['customer_name'] = self.object.get_full_name()

        return context

