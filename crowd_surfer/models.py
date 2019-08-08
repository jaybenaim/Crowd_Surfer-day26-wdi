from django.db import models 
from django.forms import ModelForm 
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date 
from django import forms 


class Project(models.Model): 
    title = models.CharField(max_length=255) 
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    funding = models.Float
class User 