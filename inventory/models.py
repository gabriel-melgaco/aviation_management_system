from django.db import models
from item.models import Item
from location.models import Location


class Inventory(models.Model):
    KANBAN_CHOICES = [
        ("ENGINE", "Motor"),
        ("CELL", "Célula"),
        ("NOT", "Não"),
    ]

    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='inventories')
    serial_number = models.CharField(max_length=20, null=True, blank=True)
    kanban = models.CharField(
        max_length=10,
        choices=KANBAN_CHOICES,
        default="COMUM"
    )    
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='location', blank=True, null=True)
    quantity = models.IntegerField(default=1)
    minimum_quantity = models.IntegerField(null=True, blank=True, default=None)
    expiration_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['location']

    def __str__(self):
        return f"NOME: {self.item.name} - MPN:{self.item.mpn} - LOC: {self.location} - SN:{self.serial_number if self.serial_number else 'Sem SN'}"

