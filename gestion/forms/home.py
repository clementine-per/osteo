from django import forms
from datetime import date, timedelta

class ConsultationStatsForm(forms.Form):
    start_date = forms.DateField(
        label="Date de début",
        initial=date.today() - timedelta(days=365),
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date = forms.DateField(
        label="Date de fin",
        initial=date.today,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    detail_type = forms.ChoiceField(
        label="Type de détail",
        choices=[
            ("animal_type", "Type d’animal"),
            ("lieu", "Lieu de consultation")
        ],
        initial="animal_type"
    )
    scale = forms.ChoiceField(
        label="Échelle",
        choices=[
            ("month", "Mois"),
            ("week", "Semaine"),
            ("day", "Jour")
        ],
        initial="month"
    )
