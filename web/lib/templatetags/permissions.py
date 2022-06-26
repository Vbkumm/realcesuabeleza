from functools import wraps
from django.urls import reverse_lazy
from django.conf import settings
from django.shortcuts import redirect
from rest_framework import permissions
from django.contrib.messages.views import messages
from businesses.models import BusinessModel


class IsBusinesssOwnerOrStaff(permissions.BasePermission):
    """
    Here I'm checking if the request.user, if the request is coming from a group that is
    allowed to perform this action or if the user here is an staff member, aka admin user.
    You can check whatever you want here since you have access to the user. So you  can
    check the sales_department like you mentioned in the question.
    """
    def has_permission(self, request, view):

        if (BusinessModel.objects.filter(slug=request.resolver_match.kwargs.get('slug'), is_active=True).exists() or request.user.is_staff):
            return True
        return False


def requires_business_owner_or_app_staff(view):

    '''
    Check if user is owner or app staff
    '''

    @wraps(view)
    def _view(request, *args, **kwargs):
        if not (BusinessModel.objects.filter(slug=request.resolver_match.kwargs.get('slug'), is_active=True).exists() or request.user.is_staff):
            messages.info(request, 'Você não tem permissão para realizar esta operação, precisa ser um proprietário')
            return redirect("%s?next=%s" % (settings.LOGIN_URL, reverse_lazy("business_detail",  kwargs={'slug': request.kwargs.get('slug')})))
        return view(request, *args, **kwargs)
    return _view