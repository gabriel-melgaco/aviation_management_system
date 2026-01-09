from django import forms
from . import models
from django.core.exceptions import ValidationError


class InflowForm(forms.ModelForm):
    class Meta:
        model = models.Inflow 
        fields = ['item', 'quantity', 'description',]
        widgets = {
            'item': forms.Select(
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
        }
        labels = {
            'item': 'Item do Estoque',
            'quantity': 'Quantidade',
            'description': 'Descrição',
        }
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity <= 0:
            raise ValidationError('A quantidade deve ser maior que 0')
        return quantity
        

class InflowAddForm(forms.ModelForm):
    class Meta:
        model = models.Inflow 
        fields = ['quantity', 'description',]
        widgets = {
            'quantity': forms.NumberInput( 
                attrs={'class': 'form-control'}
            ),
            'description': forms.TextInput( 
                attrs={'class': 'form-control'}
            ),
        }
        labels = {
            'quantity': 'Quantidade',
            'description': 'Descrição',
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity <= 0:
            raise ValidationError('A quantidade deve ser maior que 0')
        return quantity
        
