from django.contrib import admin
from . import models 


class InventoryAdmin(admin.ModelAdmin):
    list_display = ('item', 'serial_number', 'kanban', 'location', 'quantity', 'minimum_quantity', 'expiration_date')
    search_fields = ('item', 'serial_number', 'kanban', 'location', 'quantity', 'minimum_quantity', 'expiration_date')

admin.site.register(models.Inventory, InventoryAdmin)

