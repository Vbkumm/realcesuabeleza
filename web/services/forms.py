from django import forms
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


