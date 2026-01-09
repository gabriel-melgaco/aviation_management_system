from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from . import models
from inventory.models import Inventory
from django.contrib import messages
from datetime import datetime
from . import forms
from location.models import Location
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404


class OutflowListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Outflow
    template_name = 'outflow_list.html'
    context_object_name = 'outflows'
    paginate_by = 10
    permission_required = 'outflow.view_outflow'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro de busca por texto
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(inventory_item__item__name__icontains=search) |
                Q(inventory_item__item__mpn__icontains=search) |
                Q(inventory_item__item__pn__icontains=search) |
                Q(description__icontains=search)
            )
        
        # Filtro por data inicial
        date_from = self.request.GET.get('date_from')
        if date_from:
            try:
                date_from_parsed = datetime.strptime(date_from, '%Y-%m-%d').date()
                queryset = queryset.filter(created_at__date__gte=date_from_parsed)
            except ValueError:
                messages.error(self.request, 'Data inicial inválida.')
        
        # Filtro por data final
        date_to = self.request.GET.get('date_to')
        if date_to:
            try:
                date_to_parsed = datetime.strptime(date_to, '%Y-%m-%d').date()
                queryset = queryset.filter(created_at__date__lte=date_to_parsed)
            except ValueError:
                messages.error(self.request, 'Data final inválida.')
        
        # Validação: data inicial não pode ser maior que data final
        if date_from and date_to:
            try:
                date_from_parsed = datetime.strptime(date_from, '%Y-%m-%d').date()
                date_to_parsed = datetime.strptime(date_to, '%Y-%m-%d').date()
                
                if date_from_parsed > date_to_parsed:
                    messages.error(self.request, 'A data inicial não pode ser maior que a data final.')
                    # Remove os filtros inválidos
                    queryset = super().get_queryset()
                    if search:
                        queryset = queryset.filter(
                            Q(inventory_item__item__name__icontains=search) |
                            Q(inventory_item__item__mpn__icontains=search) |
                            Q(inventory_item__item__part_number__icontains=search) |
                            Q(description__icontains=search)
                        )
            except ValueError:
                pass
        
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Adiciona informações sobre os filtros ativos
        context['has_filters'] = bool(
            self.request.GET.get('search') or 
            self.request.GET.get('date_from') or 
            self.request.GET.get('date_to')
        )
        
        # Conta total de resultados
        context['total_count'] = self.get_queryset().count()
        
        return context


class OutflowDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Outflow
    template_name = 'outflow_detail.html'
    permission_required = 'outflow.view_outflow'


class OutflowMoveView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """View para registrar saída de itens do inventário"""
    permission_required = 'outflow.change_outflow'

    
    def get(self, request, pk=None):
        inventory_item = get_object_or_404(Inventory, pk=pk)

        context = {
            'item': inventory_item,
            'form_outflow': forms.OutflowForm(),
        }
        return render(request, 'outflow_move.html', context)

    def post(self, request, pk=None):
        inventory_item = get_object_or_404(Inventory, pk=pk)
        form_outflow = forms.OutflowForm(request.POST)

        if form_outflow.is_valid():
            quantity_requested = form_outflow.cleaned_data['quantity']
            claimant_requested= form_outflow.cleaned_data['claimant']
            
            # CASO 1: Item com Serial Number
            if inventory_item.serial_number:
                # Validar se quantidade é 1
                if quantity_requested != 1:
                    messages.error(
                        request, 
                        f'Itens com Serial Number só podem ter saída de 1 unidade. '
                        f'Serial Number: {inventory_item.serial_number}'
                    )
                    return render(request, 'outflow_move.html', {
                        'item': inventory_item,
                        'form_outflow': form_outflow
                    })          
                inventory_item.location = claimant_requested
                inventory_item.save()
                # Criar registro de saída
                outflow = form_outflow.save(commit=False)
                outflow.inventory_item = inventory_item
                outflow.quantity = 1
                outflow.created_by = self.request.user
                outflow.save()  
                messages.success(
                    request, 
                    f'Item com Serial Number "{inventory_item.serial_number}" '
                    f'registrado como saída com sucesso.'
                )
            # CASO 2: Item sem Serial Number (quantidade variável)
            else:
                # Validar se há estoque suficiente
                if inventory_item.quantity < quantity_requested:
                    messages.error(
                        request,
                        f'Estoque insuficiente! Disponível: {inventory_item.quantity},'
                        f'Solicitado: {quantity_requested}'
                    )
                    return render(request, 'outflow_move.html', {
                        'item': inventory_item,
                        'form_outflow': form_outflow
                    })
                
                # Reduzir quantidade do estoque
                inventory_item.quantity -= quantity_requested
                inventory_item.save()
                # Criar registro de saída
                outflow = form_outflow.save(commit=False)
                outflow.inventory_item = inventory_item  # Usar o Inventory, não o Item
                outflow.quantity = quantity_requested
                outflow.created_by = request.user
                outflow.save()
                messages.success(
                    request,
                    f'Saída de {quantity_requested} unidade(s) de'
                    f'"{inventory_item.item.name}" registrada com sucesso. '
                    f'Estoque restante: {inventory_item.quantity}'
                )
            
            return redirect('outflow_list')
        # Formulário inválido
        else:
            messages.error(request, 'Erro ao processar o formulário. Verifique os campos.')
            return render(request, 'outflow_move.html', {
                'item': inventory_item,
                'form_outflow': form_outflow
            })