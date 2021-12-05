from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import DetailView

from gestion.models.animal import Animal
from gestion.views import home, animals

urlpatterns = [
    path("", home, name="accueil"),
    path("animals/", animals.animal_list, name="animals"),
    path("animals/create", animals.CreateAnimal.as_view(), name="create_animal"),
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
]