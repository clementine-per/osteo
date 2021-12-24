from django.forms import ModelForm

from gestion.models.consultation import Consultation


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
        )

    def __init__(self, *args, **kwargs):
        super(ConsultationForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['class'] = 'datePicker'
        self.fields['date_accident'].widget.attrs['class'] = 'datePicker'