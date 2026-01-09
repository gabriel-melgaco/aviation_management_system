from django.contrib import admin
from . import models 


class ArcraftAdmin(admin.ModelAdmin):
    list_display = ('numeral', 'tsn',)
    search_fields = ('numeral', 'tsn',)

admin.site.register(models.Aircraft, ArcraftAdmin)