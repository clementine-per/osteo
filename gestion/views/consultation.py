from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from gestion.forms.consultation import ConsultationForm
from gestion.models.animal import Animal
from gestion.models.consultation import Consultation

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