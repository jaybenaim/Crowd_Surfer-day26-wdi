from django.db import models 
from django.forms import ModelForm 
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date 
from django import forms 
from django.contrib.auth.models import User 

class Project(models.Model): 
    title = models.CharField(max_length=255) 
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    funding_start_date = models.DateField() 
    funding_end_date = models.DateField() 

class Reward(models.Model): 
    reward_type = models.CharField(max_length=255)
    reward_item = models.CharField(max_length=255)
    reward_amount = models.FloatField() 

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    project = models.ForeignKey(Project, on_delete=models.CASCADE) 
    date = models.DateTimeField(auto_now=True) 
    text = models.TextField() 

class Donation(models.Model): 
    amount = models.FloatField() 
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


