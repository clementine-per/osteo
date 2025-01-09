from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django.http import HttpResponse
from django.utils.timezone import now
from datetime import timedelta
import csv
from unicodedata import normalize
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from gestion.forms.person import PersonForm, PersonSearchForm
from gestion.models.person import Person


@login_required()
def person_list(request):
    persons = Person.objects.filter(inactif=False)
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
        postal_code_form = request.GET.get("postal_code", "")
        telephone_form = request.GET.get("telephone", "")
        show_inactive = request.GET.get("show_inactive", "off") == "on"
        if show_inactive:
            persons = Person.objects.all()
        if last_name_form:
            form.fields["last_name"].initial = last_name_form
            persons = persons.filter(last_name__icontains=last_name_form)
        if city_form:
            form.fields["city"].initial = city_form
            normalized_city = normalize("NFKD", city_form).encode("ascii", "ignore").decode("utf-8").lower()
            persons = [
                person for person in persons if normalized_city in normalize("NFKD", person.city or "").encode("ascii", "ignore").decode("utf-8").lower()
            ]
        if postal_code_form:
            form.fields["postal_code"].initial = postal_code_form
            persons = persons.filter(postal_code__icontains=postal_code_form)
        if telephone_form:
            form.fields["telephone"].initial = telephone_form
            persons = persons.filter(telephone__icontains=telephone_form)
    # Pagination : Convertir en liste uniquement pour la pagination
    person_list = list(persons) if isinstance(persons, list) else persons.order_by("-update_date")
    paginator = Paginator(person_list, 20)
    try:
        page = request.GET.get("page")
        if not page:
            page = 1
        person_list = paginator.page(page)
    except EmptyPage:
        # Si on dépasse la limite de pages, on prend la dernière
        person_list = paginator.page(paginator.num_pages())

    return render(request, "gestion/person/person_list.html", locals())

@login_required
def export_new_clients_emails(request):
    current_date = now()
    first_day_of_month = current_date.replace(day=1)
    last_day_of_month = current_date.replace(
        day=1, month=current_date.month + 1 if current_date.month < 12 else 1
    ) - timedelta(days=1)
    new_clients = Person.objects.filter(
        create_date__gte=first_day_of_month,
        create_date__lte=last_day_of_month
    )
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="new_clients_emails.csv"'
    writer = csv.writer(response)
    writer.writerow(['Email'])
    for client in new_clients:
        writer.writerow([client.email])
    return response

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

@login_required
@csrf_exempt
def toggle_person_status(request, pk):
    try:
        person = Person.objects.get(pk=pk)
        person.inactif = not person.inactif
        person.save()
        return JsonResponse({"success": True, "inactif": person.inactif})
    except Person.DoesNotExist:
        return JsonResponse({"success": False, "error": "Propriétaire introuvable"}, status=404)