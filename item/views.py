from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from . import forms
from . import models
from django.db.models import Q
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.db import IntegrityError



class ItemListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Item
    template_name = 'item_list.html'
    context_object_name = 'items'
    paginate_by = 10
    permission_required = 'item.view_item'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(mpn__icontains=search) |
                Q(pn__icontains=search) |
                Q(doc__icontains=search) |
                Q(tec_pub__icontains=search)
            )

        return queryset


class ItemCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Item
    template_name = 'item_create.html'
    form_class = forms.ItemForm
    success_url = reverse_lazy('item_list')
    permission_required = 'item.add_item'


    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ItemDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Item
    template_name = 'item_detail.html'
    permission_required = 'item.view_item'



class ItemUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Item
    template_name = 'item_update.html'
    form_class = forms.ItemForm
    permission_required = 'item.change_item'


    def get_success_url(self):
        messages.success(self.request, "Item atualizado com sucesso!")
        return reverse_lazy('item_list')


class ItemDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Item
    template_name = 'item_delete.html'
    permission_required = 'item.delete_item'


    def get_success_url(self):
        return reverse_lazy('item_list')

    def post(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(self.request, "Produto deletado com sucesso!")
            return response
        except ProtectedError as e:
            messages.error(self.request, f"Não é possível deletar este produto porque ele está vinculado a outros registros.")
            return redirect('item_delete', pk=self.kwargs['pk'])
        except Exception as e:
            messages.error(self.request, f"Ocorreu um erro ao deletar: {e}")
            return redirect('item_delete', pk=self.kwargs['pk'])
        

# ----------------------ITEM EQUIVALENTS VIEWS---------------------------------------

class ItemEquivalentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.ItemEquivalent
    template_name = 'item_equivalent_list.html'
    context_object_name = 'items'
    paginate_by = 10
    permission_required = 'item.view_itemequivalent'



    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')

        if search:
            queryset = queryset.filter(
                Q(item__name__icontains=search) |
                Q(item__mpn__icontains=search) |
                Q(equivalent_item__name__icontains=search) |
                Q(equivalent_item__mpn__icontains=search)
            )

        return queryset


class ItemEquivalentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.ItemEquivalent
    template_name = 'item_equivalent_create.html'
    form_class = forms.ItemEquivalentForm
    success_url = reverse_lazy('item_list_equivalent')
    permission_required = 'item.add_itemequivalent'
    

    class ItemEquivalentCreateView(CreateView):
        model = models.ItemEquivalent
        template_name = 'item_equivalent_create.html'
        form_class = forms.ItemEquivalentForm
        success_url = reverse_lazy('item_list_equivalent')

        def form_valid(self, form):
            try:
                return super().form_valid(form)
            except IntegrityError as e:
                messages.error(self.request, f"Erro ao salvar: {e}")
                return self.form_invalid(form)


class ItemEquivalentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.ItemEquivalent
    template_name = 'item_equivalent_delete.html'
    success_url = reverse_lazy('item_list_equivalent')
    permission_required = 'item.delete_itemequivalent'



