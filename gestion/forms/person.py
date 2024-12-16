from django.forms import ModelForm, Form, CharField

from gestion.models.person import Person


class PersonSearchForm(Form):
    last_name = CharField(max_length=150, required=False, label="Nom")
    city = CharField(max_length=150, required=False, label="Ville")
    postal_code = CharField(max_length=5, required=False, label="Code Postal")
    telephone = CharField(max_length=10, required=False, label="Numéro de Téléphone")

class PersonForm(ModelForm):
    # Pour mettre les champs obligatoires en gras
    required_css_class = 'required'
    class Meta:
        model = Person
        fields = ("first_name", "last_name",\
                 "email", "address", "postal_code",\
                 "city","telephone", "commentaire",
                 "professionnel_monde_animalier")
