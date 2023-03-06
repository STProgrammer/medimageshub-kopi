from django import forms
from django.template import loader
from django.utils.safestring import mark_safe
from django_select2 import forms as s2forms

class ShareWithUsersWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "first_name__icontains",
        "last_name__icontains",
        "workplace__icontains",
    ]


class PatientSelectWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "first_name__icontains",
        "last_name__icontains",
        "city__icontains",
    ]

class MainDoctorSelectWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "first_name__icontains",
        "last_name__icontains",
        "workplace__icontains",
    ]


class ShareWidget(forms.Widget):
    template_name = 'share_widget_template.html'

    def get_context(self, name, value, attrs=None):
        return {'widget': {
            'name': name,
            'value': value,
        }}

    def render(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)