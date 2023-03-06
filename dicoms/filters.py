from django import forms
import django_filters



from .models import DicomFile, DicomFile_User, Patient


class DicomFileMyUploadsListFilter(django_filters.FilterSet):
    file_title = django_filters.CharFilter(field_name='file_title', lookup_expr='contains', label='File title')
    patient__first_name = django_filters.CharFilter(field_name='patient__first_name', lookup_expr='contains', label='Patient first name')
    patient__last_name = django_filters.CharFilter(field_name='patient__first_name', lookup_expr='contains', label='Patient last name')
    #picture_date = django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date'}), lookup_expr='contains')
    

    def __init__(self, data, *args, **kwargs):
        data = data.copy()
        data.setdefault('format', 'paperback')
        data.setdefault('order', '-added')
        super().__init__(data, *args, **kwargs)

    class Meta:
        model = DicomFile
        fields = ['file_title', 'patient__first_name', 'patient__last_name']



class DicomFileSharedListFilter(django_filters.FilterSet):
    dicomfile__file_title = django_filters.CharFilter(field_name='dicomfile__file_title', lookup_expr='contains', label='File title')
    dicomfile__patient__first_name = django_filters.CharFilter(field_name='dicomfile__patient__first_name', lookup_expr='contains', label='Patient first name')
    dicomfile__patient__last_name = django_filters.CharFilter(field_name='dicomfile__patient__last_name', lookup_expr='contains', label='Patient last name')


    def __init__(self, data, *args, **kwargs):
        data = data.copy()
        data.setdefault('format', 'paperback')
        data.setdefault('order', '-added')
        super().__init__(data, *args, **kwargs)

    class Meta:
        model = DicomFile_User
        fields = ['dicomfile__file_title', 'dicomfile__patient__first_name', 'dicomfile__patient__last_name',]


class PatientListFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='contains', label='Patient first name')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='contains', label='Patient last name')
    main_doctor__first_name = django_filters.CharFilter(field_name='main_doctor__first_name', lookup_expr='contains', label='Doctor first name')
    main_doctor__last_name = django_filters.CharFilter(field_name='main_doctor__last_name', lookup_expr='contains', label='Doctor last name')


    def __init__(self, data, *args, **kwargs):
        data = data.copy()
        data.setdefault('format', 'paperback')
        data.setdefault('order', '-added')
        super().__init__(data, *args, **kwargs)

    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'main_doctor__first_name', 'main_doctor__last_name']
