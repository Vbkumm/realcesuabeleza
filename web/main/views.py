from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


def home_view(request, *args, **kwargs):

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

    return render(request, "home.html")


class TermsView(TemplateView):
    template_name = "main/terms.html"


class CookiesView(TemplateView):
    template_name = "main/cookies.html"

