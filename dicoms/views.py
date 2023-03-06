from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.views import View
from dicoms.filters import DicomFileMyUploadsListFilter, DicomFileSharedListFilter, PatientListFilter

from dicoms.forms import CommentForm, DicomUploadForm, PatientForm, DicomShareForm, PatientUpdateForm
from users.models import User
from .models import DicomFile, DicomFile_User, Patient, Comment
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

import boto3
import medimageshub.settings as settings
from botocore.config import Config

import medimageshub.settings as settings

import json



### function to check if user has access to dicom file
def has_access_to_dicom(self):
    obj = self.get_object()
    owner = obj.owner == self.request.user
    access = self.request.user in obj.access.all()
    return owner or access


def can_edit_patient(self):
    obj = self.get_object()
    return obj.main_doctor == self.request.user


##### DCIOM Sudy View, where we use the Webnamics #####
@login_required
def dicom_study_view(request, pk):

    file_path = None
    if pk!=0:
        try:
            file_path = DicomFile.objects.get(id=pk).file_url.url
        except DicomFile.DoesNotExist:
            return render(request, "dicoms/image_not_found.html", context=context)
    
    context = {
        'file_path': file_path,
        'pk': pk,
    }
    return render(request, "dicoms/examine_image.html", context=context)



##### DICOM FILE VIEWS #####
class DicomFileUploadView(LoginRequiredMixin, CreateView):
    model = DicomFile
    form_class = DicomUploadForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(DicomFileUploadView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dicoms:dicom_detail', kwargs={'pk': self.object.id})



class DicomFileUpdateView(UserPassesTestMixin, UpdateView):
    model = DicomFile
    form_class = DicomShareForm
    template_name = 'dicoms/dicomfile_update.html'


    def form_valid(self, form):
        return super(DicomFileUpdateView, self).form_valid(form)

    
    def test_func(self):
        return has_access_to_dicom(self)

    def get_success_url(self):
        return reverse_lazy('dicoms:dicom_detail', kwargs={'pk': self.object.id})



class DicomFileDeleteView(UserPassesTestMixin, DeleteView):
    # Requires model_confirm_delete.html template name
    model = DicomFile
    success_url = reverse_lazy('users:dashboard')

    
    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user




class DicomFileMyUploadsListView(LoginRequiredMixin, ListView):
    model = DicomFile
    template_name = 'dicoms/dicomfile_my_uploads.html'
    paginate_by = 25
    context_object_name = 'dicoms_list'
    filterset_class = DicomFileMyUploadsListFilter


    def get_queryset(self):
        order = self.request.GET.get('order')
        if order is None:
            order = 'file_title'
        queryset = DicomFile.objects.filter(owner=self.request.user).order_by(order)
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()


    def get_context_data(self, **kwargs):
        context = super(DicomFileMyUploadsListView, self).get_context_data(**kwargs)
        # Pass the filterset to the template - it provides the form.
        context['filterset'] = self.filterset
        return context





class DicomFileSharedListView(LoginRequiredMixin, ListView):
    model = DicomFile_User
    template_name = 'dicoms/dicomfile_shared_list.html'
    paginate_by = 25
    context_object_name = 'shared_list'
    filterset_class = DicomFileSharedListFilter
    
    def get_queryset(self):
        order = self.request.GET.get('order')
        if order is None:
            order = 'dicomfile__file_title'
        queryset = DicomFile_User.objects.filter(user=self.request.user).order_by(order)
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super(DicomFileSharedListView, self).get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context



class DicomFileDetailView(UserPassesTestMixin, DetailView, MultipleObjectMixin):
    model = DicomFile
    template_name = 'dicoms/dicomfile_detail.html'
    context_object_name = 'dicomfile'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        comments_list = Comment.objects.filter(dicom_file=self.get_object())
        context = super(DicomFileDetailView, self).get_context_data(object_list=comments_list, **kwargs)
        context['comment_form'] = CommentForm()
        return context
    
    def test_func(self):
        return has_access_to_dicom(self)







##### COMMENT VIEWS #####

class CommentSubmit(SingleObjectMixin, UserPassesTestMixin, FormView):
    model = DicomFile
    form_class = CommentForm
    template_name = 'dicoms/dicomfile_detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CommentSubmit, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.dicom_file = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('dicoms:dicom_detail', kwargs={'pk': self.object.id})


    def test_func(self):
        return has_access_to_dicom(self)


class CommentDeleteView(UserPassesTestMixin, DeleteView):
    # Requires model_confirm_delete.html template name
    model = Comment

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def get_success_url(self):
        return reverse_lazy('dicoms:dicom_detail', kwargs={'pk': self.object.dicom_file.id})



##### PATIENT VIEWS #####

class PatientRegisterView(LoginRequiredMixin, CreateView): 
    model = Patient 
    form_class = PatientForm
    success_url = reverse_lazy('dicoms:patients_list')

    def form_valid(self, form):
        return super(PatientRegisterView, self).form_valid(form)


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient


class PatientListView(LoginRequiredMixin, ListView):
    model = Patient 
    context_object_name = 'patients_list'
    paginate_by = 25
    filterset_class = PatientListFilter
    
    def get_queryset(self):
        order = self.request.GET.get('order')
        if order is None:
            order = 'first_name'
        queryset = Patient.objects.order_by(order)
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super(PatientListView, self).get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context



class PatientUpdateView(UserPassesTestMixin, UpdateView):
    # Note! Uses model_form.html file as well
    # same form as CreateView
    model = Patient
    success_url = reverse_lazy('dicoms:patients_list')
    template_name = 'dicoms/patient_update.html'
    form_class = PatientUpdateForm


    def test_func(self):
        return can_edit_patient(self)
    

    def get_success_url(self):
        return reverse_lazy('dicoms:patient_detail', kwargs={'pk': self.object.id})



class PatientDeleteView(UserPassesTestMixin, DeleteView):
    # Requires model_confirm_delete.html template name
    model = Patient
    success_url = reverse_lazy('dicoms:patients_list')

    def test_func(self):
        return can_edit_patient(self)


