from django import forms
from .models import (ProfessionalModel,
                     ProfessionalServiceCategoryModel,
                     ProfessionalCategoryModel,
                     )


class ProfessionalCategoryForm(forms.ModelForm):
    category_professional = forms.CharField(label='',
                                            widget=forms.TextInput(attrs={'placeholder': 'Ex. Cabelereiro(a)'})
                                            )

    class Meta:
        model = ProfessionalCategoryModel
        fields = ['category_professional', ]