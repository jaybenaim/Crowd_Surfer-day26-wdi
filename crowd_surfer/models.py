from django.db import models 
from django.forms import ModelForm 
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date, datetime
from django import forms 
from django.contrib.auth.models import User 
from taggit.managers import TaggableManager
from django.db.models import Sum, Aggregate


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

    def is_expired(self):
        if self.funding_end_date < datetime.date(datetime.today()):
            return True
        else:
            return False
    
    def is_funded(self):
        total_funding = Donation.objects.filter(reward__project__pk=self.pk).aggregate(Sum('amount'))
        if total_funding['amount__sum'] == None:
            total_funding['amount__sum']=0
        
        if self.funding_goal <= total_funding['amount__sum']:
            return True
        else:
            return False

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

class Update(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="updates")
    date = models.DateTimeField(auto_now=True) 
    text = models.CharField(max_length=255)

