from django import forms
from lib.templatetags.validators import FEDERAL_ID_VALIDATE
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
                                  widget=forms.RadioSelect)

    class Meta:
        model = ProfessionalCategoryModel
        fields = ['title', 'is_active' ]


class ProfessionalFormOne(forms.ModelForm):
    name = forms.CharField(label='Qual nome do profissional?',
                           widget=forms.TextInput(attrs={'placeholder': 'Ex. Gabriela Kumm'})
                           )
    category = ProfessionalCategoryChoiceField(label='Marque as habilidades que esse profissional possui?',queryset=ProfessionalCategoryModel.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)
    birth_date = forms.DateField(label='Qual data de aniversário do profissional?', widget=forms.TextInput(attrs={'type': 'hidden', 'value': '', 'cols': 10}), required=False)

    class Meta:
        model = ProfessionalModel
        fields = ['name', 'category', 'birth_date',]


class ProfessionalFormTwo(forms.ModelForm):
    began_date = forms.DateField(label='Qual data de início do profissional?', widget=forms.TextInput(attrs={'type': 'hidden', 'value': '', 'cols': 10}), required=False)
    is_active = forms.ChoiceField(label='Profissional esta ativo?', choices=((True, 'Sim, profissional ativo.'), (False, 'Não, profissional desativo.')),
                                  widget=forms.RadioSelect)
    federal_id = forms.CharField(label='Caso não possua CNPJ informe o CPF', required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'Numero de CNPJ ou CPF'}),
                                 validators=[FEDERAL_ID_VALIDATE]
                                 )
    schedule_active = forms.ChoiceField(label='Profissional pode realizar agendamento?', choices=((True, 'Sim, profissional apto ao agendamento online.'), (False, 'Não, profissional não pode realizar agendamento.')),
                                        widget=forms.RadioSelect)
    cancel_schedule_active = forms.ChoiceField(label='Profissional pode cancelar agendamentos?', choices=((True, 'Sim, profissional pode cancelar agendamentos.'), (False, 'Não, profissional não pode cancelar agendamentos, deveram ser cancelados pela equipe.')),
                                               widget=forms.RadioSelect)

    class Meta:
        model = ProfessionalModel
        fields = ['began_date', 'federal_id', 'is_active', 'schedule_active', 'cancel_schedule_active', ]
