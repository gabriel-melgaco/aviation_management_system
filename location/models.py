from django.db import models

class LocationSite(models.Model):
    LOCATION_SITE=[
        ('internal', 'Interno'),
        ('external', 'Externo'),
    ]

    location_site = models.CharField(max_length=255)
    location_sub_site = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, choices=LOCATION_SITE)

    def __str__(self):
        return f"{self.location_site} - {self.location_sub_site}"


class Location(models.Model):
    om = models.ForeignKey(LocationSite, on_delete=models.PROTECT, related_name='location_sites')
    section = models.CharField(max_length=255, null=True, blank=True)
    shelf = models.IntegerField(null=True, blank=True)
    item_number = models.IntegerField(null=True, blank=True)
    case = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['section']
        
        constraints = [
            models.UniqueConstraint(
                fields=['om', 'section', 'shelf', 'case', 'item_number'],
                name='unique_location'
            )
        ]

    def __str__(self):
        return f"OM: {self.om} - {self.section if self.section else ''} - {self.shelf if self.shelf else ''} - {self.item_number if self.item_number else ''} - {self.case if self.case else ''}"