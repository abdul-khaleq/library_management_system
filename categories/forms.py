from django import forms
from . models import CategoriesModel

class CategoriesForm(forms.ModelForm):
    class Meta:
        model = CategoriesModel
        fields = '__all__'