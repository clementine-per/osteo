from django.db import models


class Consultation(models.Model):
    date = models.DateField()
    date_accident = models.DateField(verbose_name="Date de l’accident ou de l’apparition des symptômes",
                                     null=True, blank=True)
    reason = models.CharField(verbose_name="Motif de Consultation", max_length=300, blank=True)
    symptoms_duration = models.CharField(verbose_name="Durée des symptômes", max_length=100, blank=True)
    summary = models.TextField(verbose_name="Bilan ostéopathique", max_length=500, blank=True)
    comments = models.CharField(verbose_name="Commentaires", max_length=500, blank=True)
    animal = models.ForeignKey(
        'gestion.Animal',
        verbose_name="Animal",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return "Consultation du " + self.date.strftime("%d/%m/%Y")

    @staticmethod
    def get_first_consultation(animal):
        return Consultation.objects.filter(animal=animal).order_by('date').first()

    @staticmethod
    def get_last_consultation(animal):
        return Consultation.objects.filter(animal=animal).order_by('-date').first()

    @staticmethod
    def get_consultation_count(animal):
        return Consultation.objects.filter(animal=animal).count()