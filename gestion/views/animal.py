from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from gestion.forms.animal import AnimalForm, MedicalInfoForm, AnimalSearchForm
from gestion.models.animal import Animal, MedicalInfo
from gestion.models.person import Person


@login_required()
def animal_list(request):
    animals = Animal.objects.all()
    selected = "animals"
    title = "Liste des animaux"
    # Pagination : 20 éléments par page
    if request.method == "POST":
        form = AnimalSearchForm(request.POST)
        if form.is_valid():
            base_url = reverse('animals')
            query_string = form.data.urlencode()
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
    else:
        form = AnimalSearchForm()
        name_form = request.GET.get("name", "")
        race_form = request.GET.get("race", "")
        type_form = request.GET.get("type", "")
        if name_form:
            form.fields["name"].initial = name_form
            animals = animals.filter(name__icontains=name_form)
        if race_form:
            form.fields["race"].initial = race_form
            animals = animals.filter(race__icontains=race_form)
        if type_form:
            form.fields["type"].initial = type_form
            animals = animals.filter(type=type_form)
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
    form_class = AnimalForm
    template_name = "gestion/animal/animal_form.html"

    def get_success_url(self):
        return reverse_lazy("detail_animal", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super(CreateAnimal, self).get_context_data(**kwargs)
        context['title'] = "Créer un animal"
        return context

    def get_form(self, form_class=None):
        form = CreateView.get_form(self, form_class=form_class)
        id_proprietaire = self.request.GET.get("proprietaire", "")
        if id_proprietaire:
            proprietaire = Person.objects.get(id=id_proprietaire)
            form.fields["proprietaire"].initial = proprietaire
        return form


class UpdateAnimal(LoginRequiredMixin, UpdateView):
    model = Animal
    form_class = AnimalForm
    template_name = "gestion/animal/animal_form.html"

    def get_success_url(self):
        return reverse_lazy("detail_animal", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super(UpdateAnimal, self).get_context_data(**kwargs)
        context['title'] = "Mettre à jour " + str(self.object.name)
        return context


class UpdateMedicalInfo(LoginRequiredMixin, UpdateView):
    model = MedicalInfo
    form_class = MedicalInfoForm
    template_name = "gestion/animal/medical_info_form.html"

    def get_success_url(self):
        return reverse_lazy("detail_animal", kwargs={"pk": self.object.animal.id})

    def get_context_data(self, **kwargs):
        context = super(UpdateMedicalInfo, self).get_context_data(**kwargs)
        context['title'] = "Mettre à jour " + str(self.object.animal.name)
        return context
