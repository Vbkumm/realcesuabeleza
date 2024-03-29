from django import forms
from lib.templatetags.validators import FEDERAL_ID_VALIDATE
from services.forms import ServiceCategoryChoiceField
from services.models import ServiceCategoryModel, ServiceModel
from .models import (ProfessionalModel,
                     ProfessionalServiceCategoryModel,
                     ProfessionalCategoryModel,
                     )


class ProfessionalCategoryChoiceField(forms.ModelMultipleChoiceField):

    def __init__(self, obj_label=None, *args, **kwargs):
        super(ProfessionalCategoryChoiceField, self).__init__(*args, **kwargs)
        self.obj_label = obj_label

    def label_from_instance(self, obj):
        category_professional = obj.title
        return f'{category_professional}'


class ProfessionalCategoryForm(forms.ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Ex. Cabelereiro(a)'}))
    is_active = forms.ChoiceField(label='Categoria de profissional esta ativa?', choices=((True, 'Sim, categoria online.'), (False, 'Não, categoria offline.')),
                                  widget=forms.RadioSelect())

    class Meta:
        model = ProfessionalCategoryModel
        fields = ['title', 'is_active' ]


class ProfessionalSelectCategoryForm(forms.ModelForm):
    categories = ProfessionalCategoryChoiceField(label='Marque as habilidades que esse profissional possui?',queryset=ProfessionalCategoryModel.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)

    def __init__(self, *args, **kwargs):
        self.categories = kwargs.pop('categories', None)
        super(ProfessionalSelectCategoryForm, self).__init__(*args, **kwargs)
        if self.categories:
            self.fields['categories'].queryset = self.categories
        else:
            self.fields['categories'].choices = []
            self.fields['categories'].label = 'Primeiro adicione uma categoria de profissional!'
            self.fields['categories'].widget = forms.HiddenInput()

    class Meta:
        model = ProfessionalModel
        fields = ['categories',]


class ProfessionalFormOne(forms.ModelForm):
    title = forms.CharField(label='Qual nome do profissional?',
                           widget=forms.TextInput(attrs={'placeholder': 'Ex. Gabriela Kumm'})
                           )
    federal_id = forms.CharField(label='Caso não possua CNPJ informe o CPF', required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'Numero de CNPJ ou CPF'}),
                                 validators=[FEDERAL_ID_VALIDATE]
                                 )

    class Meta:
        model = ProfessionalModel
        fields = ['title', 'federal_id',]


class ProfessionalFormTwo(forms.ModelForm):
    birth_date = forms.DateField(label='Qual data de aniversário do profissional?', widget=forms.TextInput(attrs={'type': 'hidden', 'value': '', 'cols': 10}), required=False)

    class Meta:
        model = ProfessionalModel
        fields = ['birth_date',]

    def __init__(self, *args, **kwargs):
        self.birth_date = kwargs.pop('birth_date', None)
        super(ProfessionalFormTwo, self).__init__(*args, **kwargs)
        self.fields['birth_date'].widget.attrs['class'] = 'text-center'


class ProfessionalFormTree(forms.ModelForm):
    began_date = forms.DateField(label='Qual data de início do profissional?', widget=forms.TextInput(attrs={'type': 'hidden', 'value': '', 'cols': 10}), required=False)

    class Meta:
        model = ProfessionalModel
        fields = ['began_date',]

    def __init__(self, *args, **kwargs):
        self.began_date = kwargs.pop('began_date', None)
        super(ProfessionalFormTree, self).__init__(*args, **kwargs)
        self.fields['began_date'].widget.attrs['class'] = 'text-center'


class ProfessionalFormFour(forms.ModelForm):
    is_active = forms.ChoiceField(label='Profissional esta ativo?', choices=((True, 'Sim, profissional ativo.'), (False, 'Não, profissional desativo.')),
                                  widget=forms.RadioSelect)
    schedule_active = forms.ChoiceField(label='Profissional pode realizar agendamento?', choices=((True, 'Sim, profissional apto ao agendamento online.'), (False, 'Não, profissional não pode realizar agendamento.')),
                                        widget=forms.RadioSelect)
    cancel_schedule_active = forms.ChoiceField(label='Profissional pode cancelar agendamentos?', choices=((True, 'Sim, profissional pode cancelar agendamentos.'), (False, 'Não, profissional não pode cancelar agendamentos, deveram ser cancelados pela equipe.')),
                                               widget=forms.RadioSelect)

    class Meta:
        model = ProfessionalModel
        fields = ['is_active', 'schedule_active', 'cancel_schedule_active', ]


class ProfessionalCategoryUpdateServicesCategoryForm(forms.ModelForm):
    service_category = ProfessionalCategoryChoiceField(label='Selecione as categorias de serviço que esta categoria de profissional executa',queryset=ProfessionalCategoryModel.objects.all(), widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        self.service_category = kwargs.pop('service_category', None)
        super(ProfessionalCategoryUpdateServicesCategoryForm, self).__init__(*args, **kwargs)
        if self.service_category:
            self.fields['service_category'].queryset = self.service_category
        else:
            self.fields['service_category'].choices = []
            self.fields['service_category'].label = 'Primeiro adicione uma categoria de serviço!'
            self.fields['service_category'].widget = forms.HiddenInput()

    class Meta:
        model = ProfessionalServiceCategoryModel
        fields = ['service_category', ]


class ProfessionalSkillForm(forms.Form):
    service = forms.ModelChoiceField(queryset=ServiceModel.objects.all())
