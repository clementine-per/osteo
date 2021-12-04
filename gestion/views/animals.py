from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from gestion.forms.animals import AnimalCreateForm
from gestion.models.animal import Animal


@login_required()
def animal_list(request):
    animals = Animal.objects.all()
    selected = "animals"
    title = "Liste des animaux"
    # Pagination : 20 éléments par page
    paginator = Paginator(animals.order_by("-update_date"), 20)
    try:
        page = request.GET.get("page")
        if not page:
            page = 1
        animal_list = paginator.page(page)
    except EmptyPage:
        # Si on dépasse la limite de pages, on prend la dernière
        animal_list = paginator.page(paginator.num_pages())

    return render(request, "gestion/animal/animal_list.html", locals())

class CreateAnimal(LoginRequiredMixin, CreateView):
    model = Animal
    form_class = AnimalCreateForm
    template_name = "gestion/animal/animal_create_form.html"

    def get_success_url(self):
        return reverse_lazy("animals")

    def get_context_data(self, **kwargs):
        context = super(CreateAnimal, self).get_context_data(**kwargs)
        context['title'] = "Créer un animal"
        return context
