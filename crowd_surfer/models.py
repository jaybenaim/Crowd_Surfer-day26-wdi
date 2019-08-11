from django.db import models 
from django.forms import ModelForm 
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date 
from django import forms 
from django.contrib.auth.models import User 
from taggit.managers import TaggableManager

class Project(models.Model): 
    title = models.CharField(max_length=255) 
    description = models.TextField()
    category = models.CharField(max_length=255) 
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    funding_start_date = models.DateField() 
    funding_end_date = models.DateField()
    funding_goal = models.PositiveIntegerField()
    backers= models.ManyToManyField(User, related_name="projects_backed")
    tags = TaggableManager()

class Reward(models.Model): 
    reward_item = models.CharField(max_length=255)
    reward_description = models.TextField(null=True)
    reward_amount = models.PositiveIntegerField()
    reward_limit = models.PositiveIntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="rewards")
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    project = models.ForeignKey(Project, on_delete=models.CASCADE) 
    date = models.DateTimeField(auto_now=True) 
    text = models.CharField(max_length=255)

class Donation(models.Model): 
    amount = models.PositiveIntegerField() 
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE, related_name="donations")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')

