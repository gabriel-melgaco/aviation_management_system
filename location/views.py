from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from . import models
from django.db.models import Q
from . import forms


class LocationListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Location
    template_name = 'location_list.html'
    context_object_name = 'locations'
    paginate_by = 10
    permission_required = 'location.view_location'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')

        if search:
            queryset = queryset.filter(
                Q(om__location_site__icontains=search) |
                Q(section__icontains=search) |
                Q(shelf__icontains=search) |
                Q(item_number__icontains=search) |
                Q(case__icontains=search)
            )
            
            
        return queryset


class LocationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Location
    template_name = 'location_create.html'
    form_class = forms.LocationForm
    success_url = reverse_lazy('location_list')
    permission_required = 'location.add_location'


class LocationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Location
    template_name = 'location_update.html'
    form_class = forms.LocationForm
    success_url = reverse_lazy('location_list')
    permission_required = 'location.change_location'


    def get_success_url(self):
        messages.success(self.request, "Localização atualizada com sucesso!")
        return reverse_lazy('location_list')


class LocationDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Location
    template_name = 'location_detail.html'
    permission_required = 'location.view_location'


class LocationDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Location
    template_name = 'location_delete.html'
    success_url = reverse_lazy('location_list')
    permission_required = 'location.delete_location'

