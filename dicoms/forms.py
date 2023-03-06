from .models import DicomFile, Comment, Patient
from django import forms
from datetime import datetime, timedelta
from .widgets import ShareWithUsersWidget, PatientSelectWidget, MainDoctorSelectWidget



class DicomUploadForm(forms.ModelForm):


    class Meta:
        model = DicomFile
        fields = ('file_title', 'file_url', 'picture_date', 'patient', 'modality', 'description', 'access')

        widgets = {
            'picture_date': forms.SelectDateWidget(years=range(datetime.now().year,1849,-1)),
            'access': ShareWithUsersWidget,
            'patient': PatientSelectWidget,
            }

        help_texts = {
            'access': 'Search by first name, last name or workplace',
            'patient': 'Search by first name, last name or city',
            'file_url': 'Upload .DCM or .ZIP file'
        }


class DicomShareForm(forms.ModelForm):

    class Meta:
        model = DicomFile
        fields = ('access',)
        widgets = {
            'access': ShareWithUsersWidget,
            }
        help_texts = {
            'access': 'Search by first name, last name or workplace',
        }



class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = '__all__'

        widgets = {
            'birth_date': forms.SelectDateWidget(years=range(datetime.now().year,1849,-1)),
            'main_doctor': MainDoctorSelectWidget,
            }
        help_texts = {
            'main_doctor': 'Search by first name, last name or workplace',
        }
    

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        self.fields['height'].label = 'Height (in CMs)'


class PatientUpdateForm(forms.ModelForm):

    class Meta:
        model = Patient
        exclude = ('first_name','last_name')

        widgets = {
            'birth_date': forms.SelectDateWidget(years=range(datetime.now().year,1849,-1)),
            'main_doctor': MainDoctorSelectWidget,
            }
        help_texts = {
            'main_doctor': 'Search by first name, last name or workplace',
        }
    

    def __init__(self, *args, **kwargs):
        super(PatientUpdateForm, self).__init__(*args, **kwargs)
        self.fields['height'].label = 'Height (in CMs)'



class CommentForm(forms.ModelForm):
    http_method_names = ['get', 'post']

    class Meta:
        model = Comment
        fields = ('comment', 'image_url')
    
    def __init__(self, *args, **kwargs):
        """Save the request with the form so it can be accessed in clean_*()"""
        self.request = kwargs.pop('request', None)
        super(CommentForm, self).__init__(*args, **kwargs)

