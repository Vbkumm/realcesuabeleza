from django import forms
from django.contrib.auth import get_user_model
from .models import BusinessModel

User = get_user_model()


class BusinessUserInnForm(forms.Form):
    users = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = BusinessModel

        fields = ('users', )


class BusinessCreateForm1(forms.ModelForm):
    title = forms.CharField(label='Qual nome do seu salão?',
                                     widget=forms.TextInput(attrs={'placeholder': 'Ex. Salão da Cleide'})
                                     )
    slug = forms.CharField(label='Como gostaria de ser localizado realcesuabeleza.com.br/você?',
                            widget=forms.TextInput(attrs={'placeholder': 'seusalao'})
                            )

    class Meta:
        model = BusinessModel
        fields = ['title', 'slug', ]


class BusinessCreateForm2(forms.ModelForm):
    email = forms.EmailField(label='E-mail', max_length=254, required=False,
                             widget=forms.TextInput(attrs={'placeholder': 'email@email.com.br'})
                             )
    description = forms.CharField(label='Uma breve descrição do seu salão? poderá ser alterado no futuro',
                           widget=forms.TextInput(attrs={'placeholder': 'Descreva aqui!'})
                           )

    class Meta:
        model = BusinessModel
        fields = ['title', 'slug', ]