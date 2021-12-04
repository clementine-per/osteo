from django.forms import ModelForm

from gestion.models.animal import Animal


class AnimalCreateForm(ModelForm):
    # Pour mettre les champs obligatoires en gras
    required_css_class = 'required'
    class Meta:
        model = Animal
        fields = (
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
        super(AnimalCreateForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].widget.attrs['class'] = 'datePicker'
