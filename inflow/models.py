from django.db import models
from item.models import Item
from django.contrib.auth.models import User


class Inflow(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='items_inflows')
    quantity = models.IntegerField(default=1)
    description = models.TextField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="inflows_created")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.item}'

