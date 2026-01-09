from django.db import models
from inventory.models import Inventory
from location.models import Location
from django.contrib.auth.models import User


class Outflow(models.Model):
    inventory_item = models.ForeignKey(Inventory, on_delete=models.PROTECT, related_name='inventory_items_outflows')
    quantity = models.IntegerField(default=1)
    description = models.TextField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    claimant = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='location_outflows')
    reason = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.inventory_item}'
