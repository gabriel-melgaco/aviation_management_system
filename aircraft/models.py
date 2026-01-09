from django.db import models


class Aircraft(models.Model):
    numeral = models.CharField()
    tsn = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['numeral']

    def __str__(self):
        return f"EB{self.numeral}"
    

class Filing(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, related_name="filings")

    def __str__(self):
        return f"Filing {self.aircraft.name}"