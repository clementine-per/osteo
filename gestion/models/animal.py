from enum import Enum
from datetime import date

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


class MedicalInfo(models.Model):
    last_consult_date = models.DateField(verbose_name="Date de dernière consultation ostéopathique", null=True, blank=True)
    vaccinated = models.CharField(
        max_length=3,
        verbose_name="Vacciné(e)",
        choices=[(tag.name, tag.value) for tag in OuiNonChoice],
    )
    ape_api = models.CharField(
        max_length=3,
        verbose_name="Traité(e) APE/API",
        choices=[(tag.name, tag.value) for tag in OuiNonChoice],
    )
    antecedents = models.TextField(verbose_name="Antécédents médicaux", max_length=1000, blank=True)
    surgeries = models.TextField(verbose_name="Chirurgie(s)", max_length=300, blank=True)
    locomotor_disorders = models.CharField(verbose_name="Troubles locomoteurs", max_length=300, blank=True)
    treatments = models.TextField(verbose_name="Traitements", max_length=300, blank=True)
    behaviour = models.CharField(verbose_name="Comportement", max_length=300, blank=True)
    other = models.CharField(verbose_name="Autres", max_length=300, blank=True)


class Animal(models.Model):
    update_date = models.DateField(verbose_name="Date de mise à jour", auto_now=True)
    name = models.CharField(verbose_name="Nom", max_length=150)
    birth_date = models.DateField(verbose_name="Date de naissance", null=True, blank=True)
    race = models.CharField(verbose_name="Race", max_length=150, blank=True)
    living_place = models.CharField(verbose_name="Lieu de vie", max_length=300, blank=True)
    food = models.CharField(verbose_name="Alimentation", max_length=300, blank=True)
    activities = models.CharField(verbose_name="Activité(s)", max_length=300, blank=True)
    origin = models.CharField(verbose_name="Lieu d'adoption",
        max_length=50,
        choices=[(tag.name, tag.value) for tag in OriginChoice],
    )
    comment = models.TextField(verbose_name="Commentaire", blank=True, max_length=200)
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
    proprietaire = models.ForeignKey(
        Person,
        verbose_name="Propriétaire",
        on_delete=models.PROTECT,
    )
    # Uniquement pour les chevaux
    meadow_address = models.CharField(verbose_name="Adresse du pré", max_length=300, blank=True)
    medical_info = models.OneToOneField(MedicalInfo, on_delete=models.PROTECT)
    inactif = models.BooleanField(default=False)

    def get_age(self):
        if not self.birth_date:
            return "Âge non renseigné"
        today = date.today()
        delta = today - self.birth_date
        years = delta.days // 365
        months = (delta.days % 365) // 30
        if years < 1:
            return f"{months} mois"
        elif months == 0:
            return f"{years} an" if years == 1 else f"{years} ans"
        else:
            return f"{years} ans et {months} mois"

    def save(self, *args, **kwargs):
        # Initialisation des infos de santé à la création
        if self._state.adding:
            info = MedicalInfo.objects.create()
            self.medical_info = info
        return super(Animal, self).save(*args, **kwargs)


