from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, View
from inflow.forms import InflowForm, InflowAddForm
from inventory.forms import InventoryInflowForm
from . import models
from django.db.models import Q
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from inventory.models import Inventory
from django.shortcuts import get_object_or_404


class InflowListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Inflow
    template_name = 'inflow_list.html'
    context_object_name = 'inflows'
    paginate_by = 10
    permission_required = 'inflow.view_inflow'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro de busca por texto
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(item__name__icontains=search) |
                Q(item__mpn__icontains=search) |
                Q(item__pn__icontains=search) |
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
                            Q(item__name__icontains=search) |
                            Q(item__mpn__icontains=search) |
                            Q(item__part_number__icontains=search) |
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


class InflowCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'inflow.add_inflow'

    def get(self, request):
        context = {
            'form': InventoryInflowForm(),
            'form_inflow': InflowForm()
        }
        return render(request, "inflow_create.html", context)

    def post(self, request):
        form_inventory = InventoryInflowForm(request.POST)
        form_inflow = InflowForm(request.POST)

        if form_inventory.is_valid() and form_inflow.is_valid():
            item = form_inventory.cleaned_data['item']
            serial_number = form_inventory.cleaned_data.get('serial_number')

            if serial_number:
                # Verifica se já existe o mesmo serial_number
                inventory = Inventory.objects.filter(item=item, serial_number=serial_number).first()
                
                if inventory:
                    # Já existe → atualiza localização
                    inventory.location = form_inventory.cleaned_data['location']
                    inventory.save()
                    messages.warning(request, f'O item com Serial Number "{serial_number}" já existe. Item inserido no inventário com sucesso.')
                else:
                    # Não existe → cria novo registro
                    inventory = form_inventory.save(commit=False)
                    inventory.quantity = 1
                    inventory.minimum_quantity = 1
                    inventory.save()
            else:
                # Sem serial_number → reutiliza ou cria
                inventory = Inventory.objects.filter(item=item, serial_number__isnull=True).first()
                if not inventory:
                    inventory = form_inventory.save()
                else:
                    inventory.quantity += form_inventory.cleaned_data['quantity']
                    inventory.save()

            # Salva o inflow
            inflow = form_inflow.save(commit=False)
            inflow.item = inventory.item
            inflow.created_by = request.user
            inflow.save()

            return redirect(reverse_lazy('inflow_list'))

        # Se formulário não for válido
        return render(request, "inflow_create.html", {
            'form': form_inventory,
            'form_inflow': form_inflow
        })


class InflowAddView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'inflow.change_inflow'

    def get(self, request, pk=None):
        inventory_item = get_object_or_404(Inventory, pk=pk)

        context = {
            'item': inventory_item,
            'form_inflow': InflowAddForm(),
        }
        return render(request, 'inflow_add.html', context)

    def post(self, request, pk=None):
        inventory_item = get_object_or_404(Inventory, pk=pk)
        form_inflow = InflowAddForm(request.POST)

        if form_inflow.is_valid():
            # Atualiza a quantidade do item no inventário
            inventory_item.quantity += form_inflow.cleaned_data['quantity']
            inventory_item.save()

            # Salva um registro de entrada (Inflow)
            inflow = form_inflow.save(commit=False)
            inflow.item = inventory_item.item
            
            inflow.created_by = request.user


            inflow.save()
            
            messages.success(self.request, f'Quantidade adicionada ao item {inventory_item}')
            return redirect(reverse_lazy('inventory_list')) 

        # Se inválido, volta pro formulário
        context = {
            'item': inventory_item,
            'form_inflow': form_inflow,
        }
        return render(request, 'inflow_add.html', context)
            

class InflowDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Inflow
    template_name = 'inflow_detail.html'
    permission_required = 'inflow.view_inflow'



