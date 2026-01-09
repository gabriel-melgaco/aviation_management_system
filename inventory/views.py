from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from . import models, forms
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib import messages



class InventoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Inventory
    template_name = 'inventory_list.html'
    context_object_name = 'inventorys'
    paginate_by = 10
    permission_required = 'inventory.view_inventory'

    def get_queryset(self):

        queryset = models.Inventory.objects.all()

        site = self.kwargs.get("site")
        subsite = self.kwargs.get("subsite")

        if site and subsite:
            queryset = models.Inventory.objects.filter(
                location__om__location_site=site,
                location__om__location_sub_site=subsite
            )

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(item__mpn__icontains=search) |
                Q(item__pn__icontains=search) |
                Q(item__name__icontains=search) |
                Q(item__doc__icontains=search) |
                Q(item__tec_pub__icontains=search) |
                Q(item__aircraft_doc__icontains=search) |
                Q(location__om__location_site__icontains=search) |
                Q(location__om__location_sub_site__icontains=search) |
                Q(location__section__icontains=search) |
                Q(serial_number__icontains=search) |
                Q(kanban__icontains=search) |
                Q(item__equivalents__equivalent_item__mpn__icontains=search) |
                Q(item__equivalent_of__item__mpn__icontains=search)
            ).distinct()

        kanban = self.request.GET.get('kanban', '').strip()
        if kanban:
            queryset = queryset.filter(kanban=kanban)

        return queryset

    # se necessário enviar algum contexto específico para ao template utilizar essa função
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    
class InventoryDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Inventory
    template_name = 'inventory_detail.html'
    context_object_name = 'inventory'
    permission_required = 'inventory.view_inventory'



class InventoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Inventory
    template_name = 'inventory_update.html'
    form_class = forms.InventoryForm
    success_url = reverse_lazy('inventory_list')
    permission_required = 'inventory.change_inventory'

    
    def form_valid(self, form):
        if self.object.serial_number:
            form.instance.quantity = 1
            form.instance.minimum_quantity = 1
        
        messages.success(
            self.request, 
            f'Item "{self.object.item.name}" atualizado com sucesso!'
        )
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        if self.object.serial_number:
            if 'quantity' in form.fields:
                form.fields['quantity'].required = False
            if 'minimum_quantity' in form.fields:
                form.fields['minimum_quantity'].required = False
                
        return form
    

class InventoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Inventory
    template_name = 'inventory_delete.html'
    success_url = reverse_lazy('inventory_list')
    permission_required = 'inventory.delete_inventory'


class InventoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Inventory
    form_class = forms.InventoryForm
    success_url = reverse_lazy('inventory_list')
    permission_required = 'inventory.add_inventory'


    

