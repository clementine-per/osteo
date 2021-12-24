from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from gestion.forms.person import PersonForm, PersonSearchForm
from gestion.models.person import Person


@login_required()
def person_list(request):
    persons = Person.objects.all()
    selected = "persons"
    title = "Liste des propriétaires"
    if request.method == "POST":
        form = PersonSearchForm(request.POST)
        if form.is_valid():
            base_url = reverse('persons')
            query_string = form.data.urlencode()
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
    else:
        form = PersonSearchForm()
        last_name_form = request.GET.get("last_name", "")
        city_form = request.GET.get("city", "")
        if last_name_form:
            form.fields["last_name"].initial = last_name_form
            persons = persons.filter(last_name__icontains=last_name_form)
        if city_form:
            form.fields["city"].initial = city_form
            persons = persons.filter(city__icontains=city_form)
    # Pagination : 20 éléments par page
    paginator = Paginator(persons.order_by("-update_date"), 20)
    try:
        page = request.GET.get("page")
        if not page:
            page = 1
        person_list = paginator.page(page)
    except EmptyPage:
        # Si on dépasse la limite de pages, on prend la dernière
        person_list = paginator.page(paginator.num_pages())

    return render(request, "gestion/person/person_list.html", locals())

class CreatePerson(LoginRequiredMixin, CreateView):
    model = Person
    form_class = PersonForm
    template_name = "gestion/person/person_form.html"

    def get_success_url(self):
        return reverse_lazy("detail_person", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super(CreatePerson, self).get_context_data(**kwargs)
        context['title'] = "Créer un propriétaire"
        return context

class UpdatePerson(LoginRequiredMixin, UpdateView):
    model = Person
    form_class = PersonForm
    template_name = "gestion/person/person_form.html"

    def get_success_url(self):
        return reverse_lazy("detail_person", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super(UpdatePerson, self).get_context_data(**kwargs)
        context['title'] = "Mettre à jour " + str(self.object)
        return context