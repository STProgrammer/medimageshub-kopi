import os
from django.db import models
from .choices import Modality, Genders
from users.models import User
from django.urls import reverse 
from django_countries.fields import CountryField
from .validators import validate_file_extension

from medimageshub.storagebackends import PrivateMediaStorage
from django.core.files.storage import FileSystemStorage

class DicomFile(models.Model):

    file_url = models.FileField(
        #storage=PrivateMediaStorage(), 
        upload_to='dicoms/', validators=[validate_file_extension])

    file_title = models.CharField(max_length=256, blank=False)

    description = models.TextField(blank=True)

    picture_date = models.DateField(blank=False)
    upload_date = models.DateTimeField(auto_now_add=True)
    file_size = models.IntegerField(blank=False)
    

    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=False, related_name='owner')
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, blank=False)

    

    modality = models.CharField(choices = Modality.choices, blank=False, max_length=10)

    access = models.ManyToManyField(User, related_name='access', through='DicomFile_User', blank=True)

    def get_absolute_url(self):
        return reverse("dicoms:dicom_detail", kwargs={"pk": self.pk})

    def extension(self):
        name, extension = os.path.splitext(self.file_url.name)
        return extension

    def save(self, *args, **kwargs):
        self.file_size = self.file_url.size / 1024
        super(DicomFile, self).save(*args, **kwargs)
        

    def delete(self):
        self.file_url.delete(save=False)
        super(DicomFile, self).delete()
    
    def __str__(self):
        return f"{self.file_title}"

    class Meta:
        ordering = ['upload_date']




# Many to Many field to share files
class DicomFile_User(models.Model):
    dicomfile = models.ForeignKey(DicomFile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_time = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['added_time']



class Patient(models.Model):
    first_name = models.CharField(max_length=128, blank=False)
    last_name = models.CharField(max_length=128, blank=False)

    main_doctor = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    address = models.CharField(max_length=255, blank=False)
    postal_code = models.CharField(max_length=24, blank=False)
    city = models.CharField(max_length=64, blank=False)
    country = CountryField(blank=False)

    phone_nr = models.CharField(max_length=32, blank=True)

    birth_date = models.DateField(blank=False)
    gender = models.IntegerField(
        choices=Genders.choices,
        default=Genders.UNKNOWN,
        blank = False,
    )

    height = models.FloatField(blank=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.city})"


    def get_absolute_url(self):
        return reverse("dicoms:patient_detail", kwargs={"pk": self.pk})


    class Meta:
        ordering = ['first_name', 'last_name']


class Comment(models.Model):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=False)
    dicom_file = models.ForeignKey('DicomFile', on_delete=models.CASCADE, null=True, blank=False)
    comment = models.TextField(blank=False)
    comment_time = models.DateTimeField(auto_now_add=True)
    image_url = models.ImageField(
        #storage=PrivateMediaStorage(),
        upload_to='screenshots/', blank=True, null=True)

    def delete(self):
        self.image_url.delete(save=False)
        super(Comment, self).delete()

    class Meta:
        ordering = ['comment_time']

