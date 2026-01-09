from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages



class Item(models.Model):
    mpn = models.CharField(max_length=255, unique=True)
    pn = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    doc = models.CharField(max_length=255, null=True, blank=True)
    tec_pub = models.CharField(max_length=255, null=True, blank=True)
    aircraft_doc = models.CharField(max_length=20, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"NOME: {self.name} - MPN:{self.mpn}"
    
    @property
    def all_equivalents(self):
        eq1 = [e.equivalent_item for e in self.equivalents.all()]
        eq2 = [e.item for e in self.equivalent_of.all()]
        return set(eq1 + eq2)
    
    
class ItemEquivalent(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name="equivalents")
    equivalent_item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name="equivalent_of")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["item", "equivalent_item"], name="unique_item_equivalent"),
            models.CheckConstraint(
                check=~models.Q(item=models.F("equivalent_item")),
                name="prevent_self_equivalence"
            ),
        ]

    def clean(self):
        if ItemEquivalent.objects.filter(item=self.equivalent_item, equivalent_item=self.item).exists():
            raise ValidationError("Essa equivalência já existe na forma inversa.")

    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item} ⇔ {self.equivalent_item}"