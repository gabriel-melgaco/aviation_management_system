from django import forms
from . import models
from django.core.exceptions import ValidationError


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ['order_date', 'requester', 'order_type', 'status', 'notes']
        widgets = {
            'order_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date' 
                },
            format='%Y-%m-%d' 

            ),
            'requester': forms.Select(attrs={
                'class': 'form-control',
            }),
            'order_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,}),

        }
        labels = {
            'order_date': 'Data do pedido',
            'requester': 'Solicitante',
            'order_type': 'Tipo de Pedido',
            'status': 'Status do Pedido',
            'notes': 'Anotações',
        }


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = models.OrderItem
        fields = [
            'inventory_item',
            'item_item',
            'operator',
            'aircraft',
            'aircraft_destination',
            'service_type',
            'quantity',
            'quantity_supplied',
            'dpe',
            'eglog',
            'sn_attended',
            'expiration_date_attended',
            'log',
            'nf_answer',
            'attended_date',
            'collected',
            'gmm',
            'bms',
            'hb_destination',
            'observation',
            'notes',
            'contract_old',
            'reason',
            'troubleshooting',
            'failure_description',
            'aircraft_tsn',
            'tsn_item',
            'tso_item',
        ]

        widgets = {
            'inventory_item': forms.Select(attrs={'class': 'form-control select2'}),
            'item_item': forms.Select(attrs={'class': 'form-control select2'}),
            'operator': forms.TextInput(attrs={'class': 'form-control'}),
            'aircraft': forms.Select(attrs={'class': 'form-control'}),
            'aircraft_destination': forms.Select(attrs={'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'quantity_supplied': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'dpe': forms.TextInput(attrs={'class': 'form-control'}),
            'eglog': forms.TextInput(attrs={'class': 'form-control'}),
            'log':  forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nf_answer': forms.TextInput(attrs={'class': 'form-control'}),
            'expiration_date_attended':forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d'
            ),
            'attended_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d'
            ),
            'sn_attended':forms.TextInput(attrs={'class': 'form-control'}),
            'collected': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'gmm': forms.TextInput(attrs={'class': 'form-control'}),
            'bms': forms.TextInput(attrs={'class': 'form-control'}),
            'hb_destination': forms.TextInput(attrs={'class': 'form-control'}),
            'contract_old': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'observation': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'troubleshooting': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'failure_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tsn_item': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tso_item': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'aircraft_tsn': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

        labels = {
            'inventory_item': 'Item de Estoque (RMS)',
            'item_item': 'Item (FMS)',
            'operator': 'Nº Pedido Operador',
            'aircraft': 'Aeronave',
            'aircraft_destination': 'Aeronave de destino',
            'service_type': 'Tipo de Atendimento',
            'quantity': 'Quantidade',
            'quantity_supplied': 'Quantidade Fornecida',
            'dpe': 'DPE',
            'eglog': 'EGLOG',
            'log': 'LOG CARD',
            'expiration_date_attended': 'Data de Vencimento atendida',
            'sn_attended': 'SN Atendido',
            'nf_answer': 'Nota Fiscal de Atendimento',
            'attended_date': 'Data de Atendimento',
            'collected': 'Coletado',
            'gmm': 'GMM',
            'bms': 'BMS',
            'hb_destination': 'Destino HB',
            'contract_old': 'Contrato Anterior (013)?',
            'reason': 'Motivo',
            'observation': 'Observação',
            'notes': 'Anotações',
            'troubleshooting': 'Ação de Troubleshooting',
            'failure_description': 'Descrição da Falha',
            'tsn_item': 'TSN do Item',
            'tso_item': 'TSO do Item',
            'aircraft_tsn': 'TSN da Aeronave',
        }

    def clean(self):
        cleaned_data = super().clean()
    
        inventory_item = cleaned_data.get('inventory_item')
        item_item = cleaned_data.get('item_item')
        
        # Verifica se ambos estão preenchidos
        if inventory_item and item_item:
            raise ValidationError({
                'inventory_item': 'Você deve selecionar APENAS UM: Item de Inventário OU Item FMS.',
                'item_item': 'Você deve selecionar APENAS UM: Item de Inventário OU Item FMS.'
            })
        
        # Verifica se nenhum está preenchido
        if not inventory_item and not item_item:
            raise ValidationError({
                'inventory_item': 'Você deve selecionar pelo menos um: Item de Inventário OU Item FMS.',
                'item_item': 'Você deve selecionar pelo menos um: Item de Inventário OU Item FMS.'
            })
    
        return cleaned_data
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        
        if quantity is None or quantity <= 0:
            raise ValidationError('A quantidade deve ser maior que zero.')
        
        if quantity > 9999:
            raise ValidationError('A quantidade não pode ser maior que 9999.')
        
        return quantity