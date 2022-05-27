from django import forms
from django.contrib.auth import get_user_model
from .models import BusinessModel

User = get_user_model()


class BusinessUserInnForm(forms.Form):
    users = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = BusinessModel

        fields = ('users', )
