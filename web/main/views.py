from django.shortcuts import render
from django.views.generic import TemplateView
from lib.templatetags.permissions import flush_session
# Create your views here.


def home_view(request, *args, **kwargs):
    flush_session(request)

    return render(request, "home.html")


class TermsView(TemplateView):
    template_name = "main/terms.html"


class CookiesView(TemplateView):
    template_name = "main/cookies.html"


