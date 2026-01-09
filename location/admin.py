from django.contrib import admin
from . import models


class LocationAdmin(admin.ModelAdmin):
    list_display = ('om', 'section', 'shelf', 'item_number', 'case')
    search_fields = ('om', 'section', 'shelf', 'item_number', 'case')


admin.site.register(models.Location, LocationAdmin)

class LocationSiteAdmin(admin.ModelAdmin):
    list_display = ('location_site', 'location_sub_site', 'type',)
    search_fields = ('location_site', 'location_sub_site', 'type',)

admin.site.register(models.LocationSite, LocationSiteAdmin)
