from django.contrib.auth.models import AbstractUser, BaseUserManager ## A new class is imported. ##
from django.db import models
from datetime import datetime
from django.urls import reverse
from django_countries.fields import CountryField


class UserManager(BaseUserManager):
    """Model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Make and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Make and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Make and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    
# User model
class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(verbose_name='email address', unique=True)

    first_name = models.CharField(max_length=128, blank=False)
    last_name = models.CharField(max_length=128, blank=False)
    profession_title = models.CharField(max_length=255, blank=False)
    address = models.CharField(max_length=255, blank=False)
    postal_code = models.CharField(max_length=24, blank=False)
    city = models.CharField(max_length=64, blank=False)
    country = CountryField(blank=False)
    workplace = models.CharField(max_length=255, blank=False)
    phone_nr = models.CharField(max_length=32, blank=False)

    birth_date = models.DateField(blank=False)

    objects = UserManager()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.profession_title} from {self.workplace})"


    def get_absolute_url(self):
        return reverse("user_details", kwargs={"pk": self.pk})

    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'profession_title',
                        'country', 'city', 'postal_code','address',
                        'workplace', 'phone_nr', 'birth_date'] 
                        # Email & Password are required by default.

    class Meta:
        ordering = ['first_name', 'last_name']
