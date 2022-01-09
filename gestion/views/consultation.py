from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.dateparse import parse_date
from django.views.generic import CreateView, UpdateView

from gestion.forms.consultation import ConsultationForm, ConsultationSearchForm
from gestion.models.animal import Animal
from gestion.models.consultation import Consultation

@login_required()
def search_consultation(request):
    consultations = Consultation.objects.all()
    selected = "consultations"
    title = "Liste des consulations"

    if request.method == "POST":
        form = ConsultationSearchForm(request.POST)
        if form.is_valid():
            base_url = reverse('consultations')
            query_string = form.data.urlencode()
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
    else:
        form = ConsultationSearchForm()
        date_min_form = request.GET.get("date_min", "")
        date_max_form = request.GET.get("date_max", "")
        animal_form = request.GET.get("animal", "")
        if date_min_form:
            form.fields["date_min"].initial = date_min_form
            consultations = consultations.filter(date__gte=parse_date(date_min_form))
        if date_max_form:
            form.fields["date_max"].initial = date_max_form
            consultations = consultations.filter(date__lte=parse_date(date_max_form))
        if animal_form:
            form.fields["animal"].initial = animal_form
            consultations = consultations.filter(animal__name__icontains=animal_form)

        # Pagination : 20 éléments par page
        paginator = Paginator(consultations.order_by("-date"), 20)
        nb_results = consultations.count()
        try:
            page = request.GET.get("page")
            if not page:
                page = 1
            consultation_list = paginator.page(page)
        except EmptyPage:
            # Si on dépasse la limite de pages, on prend la dernière
            consultation_list = paginator.page(paginator.num_pages())

        return render(request, "gestion/consultation/consultation_list.html", locals())


@login_required
def create_consultation(request, pk):
    animal = Animal.objects.get(id=pk)
    title = "Créer une consultation pour " + animal.name
    if request.method == "POST":
        form = ConsultationForm(data = request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.animal = animal
            consultation.save()
            return redirect("detail_consultation", pk=consultation.id)
    else :
        form = ConsultationForm()

    return render(request, "gestion/consultation/consultation_form.html", locals())


class UpdateConsultation(LoginRequiredMixin, UpdateView):
    model = Consultation
    form_class = ConsultationForm
    template_name = "gestion/consultation/consultation_form.html"

    def get_success_url(self):
        return reverse_lazy("detail_consultation", kwargs={"pk": self.object.animal.id})

    def get_context_data(self, **kwargs):
        context = super(UpdateConsultation, self).get_context_data(**kwargs)
        context['title'] = "Mettre à jour une consultation de " + str(self.object.animal.name)
        return context