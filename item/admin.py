from django.contrib import admin
from . import models

class ItemAdmin(admin.ModelAdmin):
    list_display = ('mpn', 'pn', 'name', 'doc', 'tec_pub', 'aircraft_doc',)
    search_fields = ('mpn', 'pn', 'name', 'doc', 'tec_pub', 'aircraft_doc',)

admin.site.register(models.Item, ItemAdmin)


class ItemEquivalentAdmin(admin.ModelAdmin):
    list_display = ('item', 'equivalent_item',)
    search_fields = ('item', 'equivalent_item',)

admin.site.register(models.ItemEquivalent, ItemEquivalentAdmin)