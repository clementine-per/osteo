from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import DetailView

from gestion.models.animal import Animal
from gestion.models.consultation import Consultation
from gestion.models.person import Person
from gestion.views import home, animal, person, consultation

urlpatterns = [
    path("", home, name="accueil"),
    # Animaux
    path("animals/", animal.animal_list, name="animals"),
    path("animals/create", animal.CreateAnimal.as_view(), name="create_animal"),
    path("animals/update/<int:pk>/", animal.UpdateAnimal.as_view(), name="update_animal"),
    path(
        "animals/<int:pk>/",
        login_required(
            DetailView.as_view(
                model=Animal,
                template_name="gestion/animal/animal_detail.html",
            )
        ),
        name="detail_animal",
    ),
    path("animals/medical_info/update/<int:pk>/", animal.UpdateMedicalInfo.as_view(), name="update_medical_info"),
    # Consultations
    path("consultations/create/<int:pk>/", consultation.create_consultation, name="create_consultation"),
    path("consultations/update/<int:pk>/", consultation.UpdateConsultation.as_view(), name="update_consultation"),
    path(
        "consultations/<int:pk>/",
        login_required(
            DetailView.as_view(
                model=Consultation,
                template_name="gestion/consultation/consultation_detail.html",
            )
        ),
        name="detail_consultation",
    ),

    # Propriétaires
    path("persons/", person.person_list, name="persons"),
    path("persons/create", person.CreatePerson.as_view(), name="create_person"),
    path("persons/update/<int:pk>/", person.UpdatePerson.as_view(), name="update_person"),
    path(
        "persons/<int:pk>/",
        login_required(
            DetailView.as_view(
                model=Person,
                template_name="gestion/person/person_detail.html",
            )
        ),
        name="detail_person",
    ),
]