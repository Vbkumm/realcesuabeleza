from functools import wraps
from django.urls import reverse_lazy
from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from rest_framework import permissions
from django.contrib.messages.views import messages
from businesses.models import BusinessModel
from django.contrib.auth.decorators import login_required


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
        business = get_object_or_404(BusinessModel, slug=request.resolver_match.kwargs.get('slug'), is_active=True)
        if not request.user.is_authenticated:
            messages.info(request, 'Você não tem permissão para realizar esta operação, precisa ser um proprietário')
            return redirect("%s?next=%s" % (settings.LOGIN_URL, reverse_lazy("business_detail",  kwargs={'slug': business.slug})))
        else:
            if not (BusinessModel.objects.filter(pk=business.pk, is_active=True, owners=request.user).exists() or request.user.is_staff):
                messages.info(request, 'Você não tem permissão para realizar esta operação, precisa ser um proprietário')
                return redirect("%s?next=%s" % (settings.LOGIN_URL, reverse_lazy("business_detail",  kwargs={'slug': business.slug})))
            kwargs['id'] = business.id
            return view(request, *args, **kwargs)
    return _view


def flush_session(request):
    if 'business_slug' in request.session:
        del request.session['business_slug']
    if 'logo_qrcode_session_pk' in request.session:
        del request.session['logo_qrcode_session_pk']
    if 'nav_color' in request.session:
        del request.session['nav_color']
    if 'business_title' in request.session:
        del request.session['business_title']
    if 'text_color' in request.session:
        del request.session['text_color']
    if 'background_color' in request.session:
        del request.session['background_color']
    if 'business_name' in request.session:
        del request.session['business_name']
    if 'business_email' in request.session:
        del request.session['business_email']
    if 'business_federal_id' in request.session:
        del request.session['business_federal_id']
    if 'bg_color' in request.session:
        del request.session['bg_color']
    if 'zip_code' in request.session:
        del request.session['zip_code']
    if 'street' in request.session:
        del request.session['street']
    if 'street_number' in request.session:
        del request.session['street_number']
    if 'district' in request.session:
        del request.session['district']
    if 'city' in request.session:
        del request.session['city']
    if 'state' in request.session:
        del request.session['state']
    if 'service_category_slug' in request.session:
        del request.session['service_category_slug']
    if 'service_category_title' in request.session:
        del request.session['service_category_title']
    if 'service_slug' in request.session:
        del request.session['service_slug']
    if 'service_session' in request.session:
        del request.session['service_session']
