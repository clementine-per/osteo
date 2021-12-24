from django.db import models

from gestion.models.animal import Animal


class Consultation(models.Model):
    date = models.DateField()
    date_accident = models.DateField(verbose_name="Date de l’accident ou de l’apparition des symptômes",
                                     null=True, blank=True)
    reason = models.CharField(verbose_name="Motif de Consultation", max_length=300, blank=True)
    symptoms_duration = models.CharField(verbose_name="Durée des symptômes", max_length=100, blank=True)
    summary = models.TextField(verbose_name="Bilan ostéopathique", max_length=500, blank=True)
    animal = models.ForeignKey(
        Animal,
        verbose_name="Animal",
        on_delete=models.PROTECT,
    )