from django.urls import path

from gestion.views import home, animals

urlpatterns = [
    path("", home, name="accueil"),
    path("animals/", animals.animal_list, name="animals"),
    path("animals/create", animals.CreateAnimal.as_view(), name="create_animal"),
]