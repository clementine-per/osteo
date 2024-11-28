from django.db import models
from enum import Enum


class Consultation(models.Model):
    LIEU_CHOICES = [
        ("DOMICILE", "Domicile"),
        ("CABINET", "Cabinet"),
        ("ECURIE", "Écurie"),
    ]

    date = models.DateField()
    date_accident = models.DateField(
        verbose_name="Date de l’accident ou de l’apparition des symptômes",
        null=True, blank=True
    )
    reason = models.CharField(verbose_name="Motif de Consultation", max_length=300, blank=True)
    symptoms_duration = models.CharField(verbose_name="Durée des symptômes", max_length=100, blank=True)
    summary = models.TextField(verbose_name="Bilan ostéopathique", max_length=500, blank=True)
    comments = models.CharField(verbose_name="Commentaires", max_length=500, blank=True)
    animal = models.ForeignKey(
        'gestion.Animal',
        verbose_name="Animal",
        on_delete=models.PROTECT,
    )
    lieu = models.CharField(
        max_length=30,
        choices=LIEU_CHOICES,
        blank=True,
        null=True,
        verbose_name="Lieu de Consultation"
    )

    def display_lieu(self):
        return dict(self.LIEU_CHOICES).get(self.lieu, "")

    def __str__(self):
        return "Consultation du " + self.date.strftime("%d/%m/%Y")

