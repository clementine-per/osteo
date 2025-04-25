from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import date, timedelta
from collections import defaultdict
from django.utils.timezone import datetime

from gestion.forms.home import ConsultationStatsForm
from gestion.models.consultation import Consultation
from gestion.models.animal import AnimalTypeChoice


@login_required
def home(request):
    default_start = date.today() - timedelta(days=365)
    default_end = date.today()
    default_detail = "animal_type"
    default_scale = "month"

    if not request.GET:
        initial_data = {
            "start_date": default_start,
            "end_date": default_end,
            "detail_type": default_detail,
            "scale": default_scale
        }
        form = ConsultationStatsForm(initial=initial_data)
        start_date = default_start
        end_date = default_end
        detail_type = default_detail
        scale = default_scale
    else:
        form = ConsultationStatsForm(request.GET)
        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            detail_type = form.cleaned_data["detail_type"]
            scale = form.cleaned_data["scale"]
        else:
            start_date = default_start
            end_date = default_end
            detail_type = default_detail
            scale = default_scale

    consultations = Consultation.objects.filter(date__range=(start_date, end_date)).select_related("animal")

    data = defaultdict(lambda: defaultdict(int))

    for c in consultations:
        if not c.animal:
            continue

        if scale == "month":
            period = c.date.strftime("%Y-%m")
        elif scale == "week":
            period = c.date.strftime("%Y-W%U")
        else:
            period = c.date.strftime("%Y-%m-%d")

        key = getattr(c, "lieu") if detail_type == "lieu" else c.animal.type
        data[period][key] += 1

    chart_data = {
        "labels": sorted(data.keys()),
        "datasets": []
    }

    keys = sorted({k for d in data.values() for k in d})
    for k in keys:
        label = dict(AnimalTypeChoice.__members__).get(k, k) if detail_type == "animal_type" else k
        chart_data["datasets"].append({
            "label": label,
            "data": [data[p].get(k, 0) for p in chart_data["labels"]],
        })

    chart_title = (
        "Nombre de consultations par type d’animal"
        if detail_type == "animal_type"
        else "Nombre de consultations par lieu de consultation"
    )

    return render(request, "gestion/home.html", {
        "form": form,
        "chart_data": chart_data,
        "chart_title": chart_title
    })