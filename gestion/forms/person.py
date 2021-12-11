from django.forms import ModelForm

from gestion.models.person import Person


class PersonForm(ModelForm):
    # Pour mettre les champs obligatoires en gras
    required_css_class = 'required'
    class Meta:
        model = Person
        fields = ("first_name", "last_name",\
                 "email", "address", "postal_code",\
                 "city","telephone", "commentaire")
