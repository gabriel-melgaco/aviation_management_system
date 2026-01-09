from django import forms
from . import models


class ItemForm(forms.ModelForm):
    class Meta:
        model = models.Item
        fields = ['mpn', 'pn', 'name', 'doc', 'tec_pub', 'aircraft_doc']
        widgets = {
            'mpn':forms.TextInput(attrs={'class': 'form-control'}),
            'pn':forms.TextInput(attrs={'class': 'form-control'}),
            'name':forms.TextInput(attrs={'class': 'form-control'}),
            'doc':forms.TextInput(attrs={'class': 'form-control'}),
            'tec_pub':forms.TextInput(attrs={'class': 'form-control'}),
            'aircraft_doc':forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'mpn':'MPN',
            'pn': 'PN',
            'name': 'Nome',
            'doc': 'Manual',
            'tec_pub': 'Publicação Técnica',
            'aircraft_doc': 'Aeronave',
        }


class ItemEquivalentForm(forms.ModelForm):
    class Meta:
        model = models.ItemEquivalent
        fields = ['item', 'equivalent_item']
        
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control select2'}),
            'equivalent_item': forms.Select(attrs={'class': 'form-control select2'}),
        }
        