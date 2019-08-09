from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime 
from crowd_surfer.models import * 
from django import forms 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import authenticate
from django.urls import reverse 


def root(request): 
    return redirect('home/')
    
def home(request): 
    projects = Project.objects.all() 
    context = { 'projects': projects }
    return render(request, 'index.html', context)
    
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

def signup(request):
    form = UserCreationForm() 
    context =  {'form': form} 
    return render(request, 'registration/signup.html', context)

def signup_create(request): 
    form = UserCreationForm(request.POST)
    if form.is_valid(): 
        new_user = form.save()
        login(request, new_user)
        return redirect('/')
    else: 
        return render(request, 'registration/signup.html', {'form': form})

def project_show(request, id):
    reward_form = RewardForm()
    rewards = Project.objects.filter(pk=id).first().rewards.order_by('-reward_amount')
    context = {'project': Project.objects.get(pk=id), 'form': reward_form, 'rewards': rewards}
    return render(request, 'project.html', context)


def user_profile(request, id):
    return render(request, 'profile.html')
    pass

def project_create(request):
    if request.method == 'GET':
        context = {'form': ProjectForm(), 'action': '/projects/create'}
        return render(request, 'form.html', context)
    else:
        form = ProjectForm(request.POST)
        if  form.is_valid():
            new_proj = form.save(commit=False)
            new_proj.owner = request.user
            new_proj.save()
            return redirect(reverse('project_show', args=[new_proj.pk]))
        else:
            context = {'form': form}
            return render(request, 'form.html', context)

def back_project(request, id):
    return redirect(reverse('project_create', args=['article.id']))


def reward_create(request, id):
    form = RewardForm(request.POST)
    if form.is_valid():        
        reward = form.save(commit=False)
        project = Project.objects.get(pk=id)
        reward.project = project
        reward.save()
        return redirect(reverse('project_show', args=[id]))


