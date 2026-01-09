from django.contrib import admin
from . import models 


class OutflowAdmin(admin.ModelAdmin):
    list_display = ('inventory_item', 'quantity', 'description', 'created_at', 'updated_at', 'created_by', 'claimant', 'reason')
    search_fields = ('inventory_item', 'quantity', 'description', 'created_at', 'updated_at', 'created_by', 'claimant', 'reason')

admin.site.register(models.Outflow, OutflowAdmin)