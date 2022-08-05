from django import forms
from .models import (ServiceModel,
                     ServiceCategoryModel,
                     ServiceEquipmentModel,
                     EquipmentModel,
                     EquipmentAddressModel,)


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
        fields = ['title', 'description', 'addresses', 'is_active']

    def __init__(self, *args, **kwargs):
        self.business_address_list = kwargs.pop('business_address_list', None)
        super(EquipmentForm, self).__init__(*args, **kwargs)
        self.fields['addresses'].choices = self.business_address_list


class EquipmentAddressForm(forms.ModelForm):
    is_active = forms.BooleanField(label='Categoria ativa?', initial=True)

    class Meta:
        model = EquipmentAddressModel
        fields = ['address', 'qty', 'is_active']