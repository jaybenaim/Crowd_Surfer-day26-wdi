import datetime as dt
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.forms import  CharField, DateField, DateInput, EmailField, Form, IntegerField, ModelChoiceField, ModelForm, PasswordInput, Textarea, TextInput, TimeField, TimeInput, URLField
from crowd_surfer.models import * 
from django.forms import ModelForm 
from django import forms 


class ProjectForm(ModelForm):
    title = CharField(widget=TextInput(attrs={'class' : 'proj_title'}))
    description = CharField(widget=Textarea(attrs={'class' : 'proj_desc'}))
    funding_start_date = DateField(widget=DateInput(attrs={'type': 'date', 'min': dt.date.today(), 'class': 'fund_start_date' }))
    funding_end_date = DateField(widget=DateInput(attrs={'type': 'date', 'min': dt.date.today(), 'class': 'fund_end_date' }))

    class Meta:
        model = Project
        fields = ['title', 'description', 'funding_goal', 'funding_start_date', 'funding_end_date']
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['funding_end_date'] < cleaned_data['funding_start_date']:
            self.add_error('funding_end_date', 'Project end date must be after project start date')
        return cleaned_data


class RewardForm(ModelForm):
    reward_description = CharField(widget = Textarea(attrs={'rows':4, 'cols':15}))
    class Meta:
        model= Reward
        fields = ['reward_item', 'reward_description', 'reward_amount']
