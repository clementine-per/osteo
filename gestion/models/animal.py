from enum import Enum

from django.db import models

from gestion.models import OuiNonChoice
from gestion.models.person import Person


class AnimalTypeChoice(Enum):
    CHIEN = "Chien"
    CHAT = "Chat"
    CHEVAL = "Cheval"
    LAPIN = "Lapin"
    COCHON_INDE = "Cochon d'inde"
    CHEVRE = "Chèvre"
    MOUTON = "Mouton"
    REPTILE = "Reptile"


class SexChoice(Enum):
    F = "Femelle"
    M = "Mâle"


class OriginChoice(Enum):
    REFUGE = "Refuge"
    ELEVAGE = "Elevage"
    PARTICULIER = "Particulier"
    ANIMALERIE = "Animalerie"
    DIVAGATION = "Divagation"


class Animal(models.Model):
    update_date = models.DateField(verbose_name="Date de mise à jour", auto_now=True)
    name = models.CharField(verbose_name="Nom", max_length=150)
    race = models.CharField(verbose_name="Race", max_length=150, blank=True)
    living_place = models.CharField(verbose_name="Lieu de vie", max_length=300, blank=True)
    food = models.CharField(verbose_name="Alimentation", max_length=300, blank=True)
    activities = models.CharField(verbose_name="Activité(s)", max_length=300, blank=True)
    origin = models.CharField(verbose_name="Lieu d'adoption",
        max_length=50,
        choices=[(tag.name, tag.value) for tag in OriginChoice],
    )
    birth_date = models.DateField(verbose_name="Date de naissance", null=True, blank=True)
    adoption_age = models.CharField(verbose_name="Age d'adoption", max_length=50, blank=True)
    sex = models.CharField( verbose_name="Sexe",
        max_length=30,
        choices=[(tag.name, tag.value) for tag in SexChoice],
    )
    type = models.CharField(
        max_length=30,
        verbose_name="Espèce",
        choices=[(tag.name, tag.value) for tag in AnimalTypeChoice],
    )
    sterilised = models.CharField(
        max_length=3,
        verbose_name="Stérilisé(e)",
        choices=[(tag.name, tag.value) for tag in OuiNonChoice],
    )
    identification = models.CharField(
        max_length=150, verbose_name="Numéro d'identification", blank=True
    )
    proprietaire = models.ForeignKey(
        Person,
        verbose_name="Propriétaire",
        on_delete=models.PROTECT,
    )
    # Uniquement pour les chevaux
    meadow_address = models.CharField(verbose_name="Adresse du pré", max_length=300, blank=True)