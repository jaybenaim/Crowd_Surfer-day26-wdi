import datetime as dt
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.forms import CharField, DateField, DateInput, EmailField, Form, IntegerField, ModelChoiceField, ModelForm, PasswordInput, Textarea, TimeField, TimeInput, URLField
from crowd_surfer.models import * 
from django.forms import ModelForm 
from django import forms 


class ProjectForm(ModelForm):
    title = CharField() 
    description = Textarea()
    funding_start_date = DateField(widget=DateInput(attrs={'type': 'date', 'min': dt.date.today() }))
    funding_end_date = DateField(widget=DateInput(attrs={'type': 'date', 'min': dt.date.today() }))

    class Meta:
        model = Project
        fields = ('title', 'description', 'funding_goal', 'funding_start_date', 'funding_end_date')
        