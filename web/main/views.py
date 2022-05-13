from django.shortcuts import render

# Create your views here.


def home_view(request, *args, **kwargs):
    if 'business_slug' in request.session:
        del request.session['business_slug']

    return render(request, "home.html")
