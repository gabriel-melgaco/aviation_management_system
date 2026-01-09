from django import forms
from . import models

class LocationForm(forms.ModelForm):
    class Meta:
        model = models.Location
        fields = '__all__'
        widgets = {
            'om': forms.Select(attrs={
                'class': 'form-control',
                'style': 'background-color: #313438 !important; color: #ffffff !important;'
            }),
            'section': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Deixe em branco se não aplicável'
            }),
            'shelf': forms.TextInput(attrs={'class': 'form-control'}),
            'item_number': forms.TextInput(attrs={'class': 'form-control'}),
            'case': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'om': 'OM/Empresa Civil',
            'section': 'Seção',
            'shelf': 'Prateleira',
            'item_number': 'Número do Item',
            'case': 'Case',
        }