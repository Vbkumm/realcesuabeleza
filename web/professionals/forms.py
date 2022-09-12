from django import forms
from .models import (ProfessionalModel,
                     ProfessionalServiceCategoryModel,
                     ProfessionalCategoryModel,
                     )


class ProfessionalCategoryForm(forms.ModelForm):
    title = forms.CharField(label='',
                                            widget=forms.TextInput(attrs={'placeholder': 'Ex. Cabelereiro(a)'})
                                            )
    is_active = forms.ChoiceField(label='Categoria de profissional esta ativa?', choices=((True, 'Sim, categoria online.'), (False, 'Não, categoria offline.')),
                                  widget=forms.RadioSelect)

    class Meta:
        model = ProfessionalCategoryModel
        fields = ['title', 'is_active' ]