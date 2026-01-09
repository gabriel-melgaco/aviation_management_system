from django.contrib import admin
from . import models 


class InflowAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'description', 'created_at', 'updated_at', 'created_by',)
    search_fields = ('item', 'quantity', 'description', 'created_at', 'updated_at', 'created_by',)

admin.site.register(models.Inflow, InflowAdmin)