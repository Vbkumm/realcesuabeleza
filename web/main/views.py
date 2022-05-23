from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


def home_view(request, *args, **kwargs):
    if 'business_slug' in request.session:
        del request.session['business_slug']

    return render(request, "home.html")


class TermsView(TemplateView):
    template_name = "main/terms.html"


class CookiesView(TemplateView):
    template_name = "main/cookies.html"

