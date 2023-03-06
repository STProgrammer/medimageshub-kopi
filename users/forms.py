# users/forms.py

import hashlib
from django.contrib.auth.forms import UserCreationForm
from django.utils.crypto import get_random_string
from .models import User
from django import forms
from datetime import datetime, timedelta







