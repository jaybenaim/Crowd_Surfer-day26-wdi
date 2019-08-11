import datetime as dt
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.forms import  Select, NumberInput, ChoiceField, CharField, DateField, DateInput, EmailField, Form, IntegerField, ModelChoiceField, ModelForm, PasswordInput, Textarea, TextInput, TimeField, TimeInput, URLField
from crowd_surfer.models import * 
from django.forms import ModelForm 
from django import forms 

cat_choices = [('-----', '-----'),('Games','Games'), ('Music', 'Music'), ('Apparel', 'Apparel'), ('Random', 'Random'), ('Arts','Arts'), ('Tech' ,'Tech')]

class ProjectForm(ModelForm):
    title = CharField(widget=TextInput(attrs={'class' : 'form-title'}))
    description = CharField(widget=Textarea(attrs={'class' : 'form-description'}))
    funding_goal = IntegerField(widget=NumberInput(attrs={'class' : 'form-funding-goal'}))
    funding_start_date = DateField(widget=DateInput(attrs={'type': 'date', 'min': dt.date.today(), 'class': 'form-funding-start-date' }))
    funding_end_date = DateField(widget=DateInput(attrs={'type': 'date', 'min': dt.date.today(), 'class': 'form-funding-end-date' }))
    category = ChoiceField(choices=cat_choices, widget=forms.Select(attrs={'class':'form-category'}))

    class Meta:
        model = Project
        fields = ['title', 'description','category', 'funding_goal', 'funding_start_date', 'funding_end_date', 'tags']
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['funding_end_date'] < cleaned_data['funding_start_date']:
            self.add_error('funding_end_date', 'Project end date must be after project start date')
        return cleaned_data


class RewardForm(ModelForm):
    reward_description = CharField(widget = Textarea(attrs={'rows':4, 'cols':15}))
    
    class Meta:
        model= Reward
        fields = ['reward_item', 'reward_description', 'reward_amount', 'reward_limit']

