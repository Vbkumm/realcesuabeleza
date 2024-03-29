from django import forms
from django.core.validators import RegexValidator
from realcesuabeleza.settings import WEEKDAYS_CHOICES
from django.contrib.auth import get_user_model
from localflavor.br.forms import BRZipCodeField
from lib.templatetags.validators import FEDERAL_ID_VALIDATE
from .models import (BusinessModel,
                     BusinessAddressModel,
                     BusinessPhoneModel,
                     BusinessLogoQrcodeModel,
                     BusinessAddressHoursModel)


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


class BusinessLogoQrcodeForm(forms.ModelForm):
    logo_img = forms.ImageField(label='',)

    def __init__(self, *args, **kwargs):
        super(BusinessLogoQrcodeForm, self).__init__(*args, **kwargs)
        self.fields['logo_img'].widget.attrs.update({'onchange': "readURL(this);",})

    class Meta:
        model = BusinessLogoQrcodeModel
        fields = ['logo_img',]


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


class BusinessPhoneForm(forms.ModelForm):
    phone = forms.CharField(label='Numero do telefone', max_length=150, required=False,)

    class Meta:
        model = BusinessPhoneModel
        fields = ['phone', 'is_whatsapp',]


class BusinessAddressHoursForm(forms.ModelForm):

    week_days = forms.ChoiceField(label='Dia da semana', choices=WEEKDAYS_CHOICES)
    start_hour = forms.TimeField(label='Qual primeiro horário para agendamento?', widget=forms.TimeInput(format='%H:%M'), initial='09:00')
    end_hour = forms.TimeField(label='Qual ultimo horário para agendamento?', widget=forms.TimeInput(format='%H:%M'), initial='19:00')
    is_active = forms.BooleanField(label='Dia esta ativo?', initial=True)

    def __init__(self, *args, **kwargs):
        self.business_address_day_list = kwargs.pop('business_address_day_list', None)
        super(BusinessAddressHoursForm, self).__init__(*args, **kwargs)
        self.fields['week_days'].choices = sorted(list({(k, v) for k, v in WEEKDAYS_CHOICES}))

    def clean(self):
        super(BusinessAddressHoursForm, self).clean()
        business_address_day_list = self.business_address_day_list
        week_days = self.cleaned_data['week_days']
        start_hour = self.cleaned_data['start_hour']
        end_hour = self.cleaned_data['end_hour']
        if end_hour <= start_hour:
            raise forms.ValidationError(f'A hora final {end_hour} tem que ser superior {start_hour} hora inicial!')
        if business_address_day_list:
            for business_address_hour in business_address_day_list:
                if business_address_hour.week_days == int(week_days):
                    if business_address_hour.start_hour >= start_hour <= business_address_hour.end_hour:
                        raise forms.ValidationError(f'A hora inicial {start_hour} esta entre horários inicio {business_address_hour.start_hour} e final  {business_address_hour.end_hour}. Talvez esse horário esteja desativado.')
                    if business_address_hour.start_hour >= end_hour <= business_address_hour.end_hour:
                        raise forms.ValidationError(f'A hora final {end_hour}  não pode estar entre {business_address_hour.start_hour} e {business_address_hour.end_hour} pois já existe nesta data. Talvez esse horário esteja desativado')

    class Meta:
        model = BusinessAddressHoursModel
        fields = ['week_days', 'start_hour', 'end_hour', 'is_active', ]

