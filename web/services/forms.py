from django import forms
from realcesuabeleza.settings import CHOICES_MIN_TIME
from businesses.models import BusinessAddressModel
from .models import (ServiceModel,
                     ServiceCategoryModel,
                     ServiceEquipmentModel,
                     EquipmentModel,
                     EquipmentAddressModel,)


class BusinessAddressChoiceField(forms.ModelChoiceField):

    def __init__(self, obj_label=None, *args, **kwargs):
        super(BusinessAddressChoiceField, self).__init__(*args, **kwargs)
        self.obj_label = obj_label

    def label_from_instance(self, obj):
        return f'{obj.zip_code} - {obj.street}'


class ServiceCategoryChoiceField(forms.ModelChoiceField):

    def __init__(self, obj_label=None, *args, **kwargs):
        super(ServiceCategoryChoiceField, self).__init__(*args, **kwargs)
        self.obj_label = obj_label

    def label_from_instance(self, obj):
        return obj.title


class ProfessionalCategoryChoiceField(forms.ModelChoiceField):

    def __init__(self, obj_label=None, *args, **kwargs):
        super(ProfessionalCategoryChoiceField, self).__init__(*args, **kwargs)
        self.obj_label = obj_label

    def label_from_instance(self, obj):
        return obj.category_professional


class EquipmentField(forms.ModelChoiceField):

    def __init__(self, obj_label=None, *args, **kwargs):
        super(EquipmentField, self).__init__(*args, **kwargs)
        self.obj_label = obj_label

    def label_from_instance(self, obj):
        return f'{obj.title}'


class ServiceCategoryForm(forms.ModelForm):
    is_active = forms.BooleanField(label='Categoria ativa?', initial=True)

    class Meta:
        model = ServiceCategoryModel
        fields = ['title', 'is_active']


class EquipmentForm(forms.ModelForm):
    is_active = forms.BooleanField(label='Categoria ativa?', initial=True)

    class Meta:
        model = EquipmentModel
        fields = ['title', 'description', 'is_active']


class EquipmentAddressForm(forms.ModelForm):
    is_active = forms.BooleanField(label='Categoria ativa?', initial=True)
    address = BusinessAddressChoiceField(label='Selecione o endereço deste equipamento',
                                           queryset=BusinessAddressModel.objects.all(),
                                           empty_label="(Add uma nova se nåo encontrar)",
                                           required=False,
                                           initial=0,)

    class Meta:
        model = EquipmentAddressModel
        fields = ['address', 'qty', 'is_active']

    def __init__(self, *args, **kwargs):
        self.address = kwargs.pop('address', None)
        super(EquipmentAddressForm, self).__init__(*args, **kwargs)
        self.fields['address'].choices = self.address


class ServiceFormOne(forms.ModelForm):
    service_category = ServiceCategoryChoiceField(label='Selecione uma catergoria de serviço',
                                                  queryset=ServiceCategoryModel.objects.all(),
                                                  empty_label="(Add uma nova se nåo encontrar)",
                                                  )
    title = forms.CharField(label='Qual nome do serviço?',
                            widget=forms.TextInput(attrs={'placeholder': 'Ex. Coloração'})
                            )

    class Meta:
        model = ServiceModel
        fields = ['service_category', 'title', ]


class ServiceFormTwo(forms.ModelForm):
    description = forms.CharField(label='', widget=forms.Textarea(
        attrs={'rows': 4, 'placeholder': 'Aqui você pode descrever melhor o serviçø com até 1000 caracteres.'}
    ),
                                          max_length=1000,
                                          help_text='Número maximo de caracteres 1000.'
                                          )
    is_active = forms.ChoiceField(label='Este serviço esta ativo?', choices=((True, 'Sim, serviço online.'), (False, 'Não, serviço offline.')),
                                       widget=forms.RadioSelect)
    schedule_active = forms.ChoiceField(label='Serviço pode ser agendado por clintes?', choices=((True, 'Sim, serviço com agendamento online.'), (False, 'Não, serviço so pode ser agendo pela equipe.')),
                                                widget=forms.RadioSelect)
    cancel_schedule_active = forms.ChoiceField(label='Agendamento deste serviço pode ser cancelado por clintes?', choices=((True, 'Sim, serviço com cancelamento de agendamento online.'), (False, 'Não, serviço so pode ter agendamento cancelado pela equipe.')),
                                                       widget=forms.RadioSelect)

    class Meta:
        model = ServiceModel
        fields = ['description', 'is_active', 'schedule_active', 'cancel_schedule_active',]


class ServiceEquipmentForm(forms.ModelForm):
    equipment = EquipmentField(label='Selecione um equipamento para realizar o serviço, lembrando que você pode adicionar um novo ou ativar um equipamento ja cadastrado caso não encontre na lista.',
                               queryset=EquipmentModel.objects.all(),
                               empty_label="Lista de equipamentos cadastrados e ativos.",
                               required=True,
                               )
    equipment_time = forms.IntegerField(label='Qual tempo de utilização do equipamento?', widget=forms.Select(choices=CHOICES_MIN_TIME), required=True)
    equipment_complement = forms.ChoiceField(label='Este equipamento é usado simutaniamente com algum outro equipamento?', choices=((True, 'Sim, o equipamento é usado em conjunto com o equipamento que escolherei a seguir.'), (False, 'Não, este equipamento faz parte de uma etapa do serviço e não complementa nenhum.')),
                                             widget=forms.RadioSelect)

    equipment_replaced = EquipmentField(label='Caso tenha marcado sim para opção a anterior, ou se marcou não e deseja incluir este equipamento como substitudo para outro, selecione aqui o equipamento',
                                              queryset=EquipmentModel.objects.all(),
                                              empty_label="Se sim, escolha um equipamento",
                                              required=False,
                                           )

    def __init__(self, *args, **kwargs):
        self.equipment_replaced = kwargs.pop('equipment_replaced', None)
        self.equipment = kwargs.pop('equipment', None)
        super(ServiceEquipmentForm, self).__init__(*args, **kwargs)
        if self.equipment_replaced:
            self.fields['equipment_complement'].required = True
            self.fields['equipment_replaced'].queryset = self.equipment_replaced
        else:
            self.fields['equipment_replaced'].label = ""
            self.fields['equipment_replaced'].widget = forms.HiddenInput()
            self.fields['equipment_complement'].widget = forms.HiddenInput()
            self.fields['equipment_complement'].initial = False
            self.fields['equipment_complement'].label = ""
        self.fields['equipment'].queryset = self.equipment

    def clean(self):
        cleaned_data = super().clean()
        equipment_complement = cleaned_data.get('equipment_complement')
        equipment_replaced = cleaned_data.get('equipment_replaced')
        if equipment_complement:
            if not equipment_replaced and equipment_complement == 'True':
                raise forms.ValidationError(f'Necessario escolher equipamento que é usado simutaniamente!')
        else:
            raise forms.ValidationError(f'Necessario responder se este equipamento é usado simutaniamente com algum outro equipamento!')

    class Meta:
        model = ServiceEquipmentModel
        fields = ['equipment', 'equipment_time', 'equipment_complement', 'equipment_replaced', ]
