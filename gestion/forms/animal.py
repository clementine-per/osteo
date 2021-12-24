from django.db.models import BLANK_CHOICE_DASH
from django.forms import ModelForm, Form, CharField, ChoiceField, Select

from gestion.models.animal import Animal, MedicalInfo, AnimalTypeChoice
from gestion.models.person import Person


class AnimalSearchForm(Form):
    name = CharField(max_length=150, required=False, label="Nom")
    type = ChoiceField(
        choices=BLANK_CHOICE_DASH + [(tag.name, tag.value) for tag in AnimalTypeChoice],
        widget=Select(),
        required=False,
    )
    race = CharField(max_length=150, required=False, label="Race")


class AnimalForm(ModelForm):
    # Pour mettre les champs obligatoires en gras
    required_css_class = 'required'
    class Meta:
        model = Animal
        fields = (
            "proprietaire",
            "name",
            "sex",
            "type",
            "race",
            "living_place",
            "food",
            "activities",
            "origin",
            "birth_date",
            "adoption_age",
            "sterilised",
            "identification",
            "meadow_address",
        )

    def __init__(self, *args, **kwargs):
        super(AnimalForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].widget.attrs['class'] = 'datePicker'
        self.fields["proprietaire"].queryset = Person.objects.order_by('last_name')


class MedicalInfoForm(ModelForm):
    # Pour mettre les champs obligatoires en gras
    required_css_class = 'required'
    class Meta:
        model = MedicalInfo
        fields = (
            "last_consult_date",
            "vaccinated",
            "ape_api",
            "antecedents",
            "surgeries",
            "locomotor_disorders",
            "past_treatments",
            "current_treatments",
            "behaviour",
            "other",
        )

    def __init__(self, *args, **kwargs):
        super(MedicalInfoForm, self).__init__(*args, **kwargs)
        self.fields['last_consult_date'].widget.attrs['class'] = 'datePicker'
