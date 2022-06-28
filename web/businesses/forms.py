from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from localflavor.br.forms import BRZipCodeField
from lib.templatetags.validators import FEDERAL_ID_VALIDATE
from .models import BusinessModel, BusinessAddressModel


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
    slug = forms.CharField(label='Como gostaria de ser localizado? realcesuabeleza.com.br/você?',
                            widget=forms.TextInput(attrs={'placeholder': 'seu_salao'})
                            )

    def __init__(self, *args, **kwargs):
        super(BusinessCreateForm1, self).__init__(*args, **kwargs)
        self.fields['title'].required = True

    class Meta:
        model = BusinessModel
        fields = ['title', 'slug', ]


class BusinessCreateForm2(forms.ModelForm):
    federal_id = forms.CharField(label='Caso não possua CNPJ informe seu CPF', required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'Numero de CNPJ ou CPF'}),
                                 validators=[FEDERAL_ID_VALIDATE]
                                 )

    email = forms.EmailField(label='E-mail', max_length=254, required=False,
                             widget=forms.TextInput(attrs={'placeholder': 'email@email.com.br'})
                             )

    def __init__(self, *args, **kwargs):
        super(BusinessCreateForm2, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['federal_id'].required = True

    class Meta:
        model = BusinessModel
        fields = ['federal_id', 'email',]


class BusinessCreateForm3(forms.ModelForm):

    description = forms.CharField(label='Uma breve descrição do seu salão? poderá ser alterado no futuro', widget=forms.Textarea(
        attrs={'rows': 4, 'placeholder': 'Descreva aqui seu salão em até 1000 caracteres.'}),
                                  max_length=1000,
                                  help_text='Número maximo permitido de caracteres 1000.'
                                  )

    class Meta:
        model = BusinessModel
        fields = ['description', ]


class BusinessCreateForm4(forms.ModelForm):
    birth_date = forms.EmailField(label='E-mail', max_length=254, required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'email@email.com.br'})
                                  )

    def __init__(self, *args, **kwargs):
        super(BusinessCreateForm4, self).__init__(*args, **kwargs)
        self.fields['birth_date'].required = True

    class Meta:
        model = BusinessModel
        fields = ['birth_date', ]


class BusinessAddressForm1(forms.ModelForm):
    zip_code = BRZipCodeField(label='CEP', max_length=9, required=False)
    street = forms.CharField(label='Rua', max_length=100, required=False)
    district = forms.CharField(label='', max_length=100, required=False)
    city = forms.CharField(label='', max_length=100, required=False)
    state = forms.CharField(label='', max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super(BusinessAddressForm1, self).__init__(*args, **kwargs)
        self.fields['district'].widget = forms.HiddenInput()
        self.fields['city'].widget = forms.HiddenInput()
        self.fields['state'].widget = forms.HiddenInput()
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'col-md-6'

    class Meta:
        model = BusinessAddressModel

        fields = ['zip_code', 'street', ]


class BusinessAddressForm2(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.zip_code = kwargs.pop('zip_code', None)
        super(BusinessAddressForm2, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'col-md-6'

    class Meta:
        model = BusinessAddressModel

        fields = ['street_number', 'complement',]


class BusinessAddressForm3(forms.ModelForm):
    district = forms.CharField(label='Bairro', max_length=100, required=False)
    city = forms.CharField(label='Cidade', max_length=100, required=False)
    state = forms.CharField(label='Estado', max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        self.district = kwargs.pop('district', None)
        self.city = kwargs.pop('city', None)
        self.state = kwargs.pop('state', None)
        super(BusinessAddressForm3, self).__init__(*args, **kwargs)
        self.fields['district'].initial = self.district
        self.fields['city'].initial = self.city
        self.fields['state'].initial = self.state
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'col-md-6'

    class Meta:
        model = BusinessAddressModel

        fields = ['district', 'city', 'state', ]
