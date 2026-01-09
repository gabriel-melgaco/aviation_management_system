from django import forms
from . import models
from django.core.exceptions import ValidationError
from inventory.models import Inventory


class OutflowForm(forms.ModelForm):
    class Meta:
        model = models.Outflow
        fields = [ 'quantity', 'description', 'claimant', 'reason']

        widgets = {
            'claimant': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'background-color: #313438 !important; color: #ffffff !important;'
                }
            ),
            'quantity': forms.NumberInput( 
                attrs={'class': 'form-control'}
            ),
            'description': forms.TextInput( 
                attrs={'class': 'form-control'}
            ),
            'reason': forms.TextInput(attrs={'class': 'form-control'}
            ),
        }
        labels = {
            'claimant': 'Solicitante',
            'quantity': 'Quantidade',
            'description': 'Descrição',
            'reason': 'motivo',
        }
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity <= 0:
            raise ValidationError('A quantidade deve ser maior que 0')
        return quantity