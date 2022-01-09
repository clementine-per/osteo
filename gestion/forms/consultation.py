from django.forms import ModelForm, DateField, Form, CharField

from gestion.forms import DateInput
from gestion.models.consultation import Consultation


class ConsultationSearchForm(Form):
    date_min = DateField(
        label="Date de consultation entre le", required=False, widget=DateInput()
    )
    date_max = DateField(
        label="et le", required=False, widget=DateInput()
    )
    animal = CharField(required=False, max_length=150)


class ConsultationForm(ModelForm):
    # Pour mettre les champs obligatoires en gras
    required_css_class = 'required'
    class Meta:
        model = Consultation
        fields = (
            "date",
            "date_accident",
            "reason",
            "symptoms_duration",
            "summary",
            "comments",
        )

    def __init__(self, *args, **kwargs):
        super(ConsultationForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['class'] = 'datePicker'
        self.fields['date_accident'].widget.attrs['class'] = 'datePicker'