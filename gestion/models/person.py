from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from gestion.models.consultation import Consultation


class Person(models.Model):
    update_date = models.DateField(verbose_name="Date de mise à jour", auto_now=True)
    create_date = models.DateField(verbose_name="Date de création", auto_now_add=True, default=timezone.now)
    first_name = models.CharField(verbose_name="Prénom",max_length=30)
    last_name = models.CharField(verbose_name="Nom",max_length=150)
    email = models.EmailField(max_length=150, blank=True)
    address = models.CharField(verbose_name="Adresse", max_length=500)
    postal_code_regex = RegexValidator(
        regex="^[0-9]*$", message="Veuillez entrer un code postal valide."
    )
    postal_code = models.CharField(verbose_name="Code postal", validators=[postal_code_regex], max_length=5)
    city = models.CharField(verbose_name="Ville",max_length=100)
    telephone_regex = RegexValidator(
        regex="[0-9]{10}", message="Veuillez entrer un numéro de téléphone valide."
    )
    telephone = models.CharField(validators=[telephone_regex], max_length=10)
    commentaire = models.CharField(max_length=1000, blank=True)
    inactif = models.BooleanField(
        default=False,
        verbose_name="Desactivé (Ne cocher que si vous ne souhaitez\
                                       plus gérer cette personne dans l'application) ",
    )


    def get_complete_address(self):
        return f"{self.address} \n {self.postal_code} {self.city}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_all_consultations(self):
        return Consultation.objects.filter(animal__proprietaire=self)

    def get_first_consultation_date(self):
        first_consultation = self.get_all_consultations().order_by('date').first()
        return first_consultation.date if first_consultation else None

    def get_last_consultation_date(self):
        last_consultation = self.get_all_consultations().order_by('-date').first()
        return last_consultation.date if last_consultation else None

    def get_total_consultations(self):
        return self.get_all_consultations().count()