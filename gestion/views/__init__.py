import calendar
import locale

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.urls import reverse
from django.utils.timezone import datetime


from gestion.models.consultation import Consultation



@login_required
def home(request):
    # Partie Consultations
    labels_mois = []
    # Consultations pour l'année en cours
    data_consultations_current = []
    # Consultations pour l'année précédente
    data_consultations_past = []

    consultations = Consultation.objects.all()
    # Pour que les mois soient en français
    locale.setlocale(locale.LC_ALL, 'fr_FR')
    date = datetime.now()

    i = 1
    current = date.year
    past = date.year - 1

    while (i < 13):
        labels_mois.append(calendar.month_name[i])
        data_consultations_current.append(consultations.filter(date__year=date.year).filter(date__month=i).count())
        data_consultations_past.append(consultations.filter(date__year=date.year - 1).filter(date__month=i).count())
        i += 1
    return render(request, "gestion/home.html", locals())