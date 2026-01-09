from django import forms
from . import models


class InventoryForm(forms.ModelForm):
    class Meta:
        model = models.Inventory  
        fields = ['kanban', 'serial_number', 'location', 'quantity', 'minimum_quantity', 'expiration_date']
        widgets = {
            
            'kanban': forms.Select(
                attrs={
                    'class': 'form-control',
                    'style': 'background-color: #313438 !important; color: #ffffff !important;'
                }
            ),
            'location': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'background-color: #313438 !important; color: #ffffff !important;'
                }
            ),
            'quantity': forms.NumberInput( 
                attrs={'class': 'form-control'}
            ),
            'serial_number': forms.TextInput( 
                attrs={'class': 'form-control'}
            ),
            'minimum_quantity': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
            'expiration_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date' 
                },
            format='%Y-%m-%d' 

            ),
        }
        labels = {
            'item': 'Item',
            'kanban': 'Kanban',
            'serial_number': 'Serial Number',
            'location': 'Localização',
            'quantity': 'Quantidade',
            'minimum_quantity': 'Quantidade Mínima',
            'expiration_date': 'Data de Validade',
        }

        def clean(self):
            cleaned_data = super().clean()
            
            if hasattr(self.instance, 'serial_number') and self.instance.serial_number:
                cleaned_data['quantity'] = 1
                cleaned_data['minimum_quantity'] = 1
                
            return cleaned_data
    
        def save(self, commit=True):
            instance = super().save(commit=False)
            
            if instance.serial_number:
                instance.quantity = 1
                instance.minimum_quantity = 1
                
            if commit:
                instance.save()
            return instance



class InventoryInflowForm(forms.ModelForm):
    class Meta:
        model = models.Inventory  
        fields = ['item', 'kanban', 'serial_number', 'location', 'quantity', 'minimum_quantity', 'expiration_date']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control select2',
                                        'style': 'background-color: #313438 !important; color: #ffffff !important;'
                                        }),
            'kanban': forms.Select(
                attrs={
                    'class': 'form-control',
                    'style': 'background-color: #313438 !important; color: #ffffff !important;'
                }
            ),
            'location': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'background-color: #313438 !important; color: #ffffff !important;'
                }
            ),
            'quantity': forms.NumberInput( 
                attrs={'class': 'form-control'}
            ),
            'serial_number': forms.TextInput( 
                attrs={'class': 'form-control'}
            ),
            'minimum_quantity': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
            'expiration_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date' 
                },
            format='%Y-%m-%d' 

            ),
        }
        labels = {
            'item': 'Item',
            'kanban': 'Kanban',
            'serial_number': 'Serial Number',
            'location': 'Localização',
            'quantity': 'Quantidade',
            'minimum_quantity': 'Quantidade Mínima',
            'expiration_date': 'Data de Validade',
        }

        def clean(self):
            cleaned_data = super().clean()
            
            if hasattr(self.instance, 'serial_number') and self.instance.serial_number:
                cleaned_data['quantity'] = 1
                cleaned_data['minimum_quantity'] = 1
                
            return cleaned_data
    
        def save(self, commit=True):
            instance = super().save(commit=False)
            
            if instance.serial_number:
                instance.quantity = 1
                instance.minimum_quantity = 1
                
            if commit:
                instance.save()
            return instance
        


