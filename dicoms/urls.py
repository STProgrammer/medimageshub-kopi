from django.urls import path, include
from . import views

app_name = 'dicoms'

urlpatterns = [
    path('upload/',views.DicomFileUploadView.as_view(),name='dicom_upload'),
    path('my-uploads/',views.DicomFileMyUploadsListView.as_view(),name='dicom_my_uploads_list'),
    path('shared/',views.DicomFileSharedListView.as_view(),name='dicom_shared_list'),
    path('details/<int:pk>/',views.DicomFileDetailView.as_view(),name='dicom_detail'),
    path('update/<int:pk>/',views.DicomFileUpdateView.as_view(),name='dicom_update'),
    path('details/<int:pk>/post-comment',views.CommentSubmit.as_view(),name='comment_post'),
    path('details/delete-comment/<int:pk>',views.CommentDeleteView.as_view(),name='comment_delete'),
    path('delete/<int:pk>/', views.DicomFileDeleteView.as_view(),name='dicom_delete'),
    path('study/<int:pk>/', views.dicom_study_view, name='dicom_study'),

    path('patients/add',views.PatientRegisterView.as_view(), name='patient_add'),
    path('patients/details/<int:pk>/',views.PatientDetailView.as_view(),name='patient_detail'),
    path('patients/',views.PatientListView.as_view(), name='patients_list'),
    path('patients/delete/<int:pk>/',views.PatientDeleteView.as_view(),name='patient_delete'),
    path('patients/update/<int:pk>/',views.PatientUpdateView.as_view(),name='patient_update'),
    ]