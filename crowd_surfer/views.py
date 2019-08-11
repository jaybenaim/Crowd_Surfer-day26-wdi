
from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Aggregate
from datetime import datetime 
from crowd_surfer.models import * 
from django import forms 
from crowd_surfer.forms import * 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm 
from django.db.models import Q
import datetime

from django.urls import reverse 

def root(request): 
    return redirect('home/')
    
def home(request): 
    return render(request, 'index.html', {
        'projects': Project.objects.all() 
    })
    
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            
            user = authenticate(username=username, password=pw)
            
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/home')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()

    return render(request, 'login.html', {
        'form': form
    }) 


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
    project = Project.objects.get(pk=id)
    reward_form = RewardForm()
    rewards = Project.objects.filter(pk=id).first().rewards.order_by('-reward_amount')
    donations = Donation.objects
    total_donations = Donation.objects.all().aggregate(Sum('amount'))
    funding_end_date = project.funding_end_date 
    delta = datetime.datetime(funding_end_date.year, funding_end_date.month, funding_end_date.day) - datetime.datetime.now()

    context = {
        'project': project,
        'form': reward_form,
        'rewards': rewards, 
        'total_donations': total_donations['amount__sum'], 
        'delta': delta,
        }

    return render(request, 'project.html', context)

@login_required
def profile_show(request, id):
    projects = Project.objects.filter(owner_id=id)
    backers = Project.backers
    donations = Donation.objects.filter(reward__project__owner_id=id)
    total_donations = Donation.objects.filter(reward__project__backers=id).aggregate(Sum('amount'))

    total_recieved = 0 
    for donation in donations:
        total_recieved += donation.amount 

    return render(request, 'profile.html', { 
        'projects': projects, 
        'backers': backers,
        'project_donations': donations,
        'donations': total_donations,
        'total_recieved' : total_recieved,
    })
    
def profiles(request): 
    users = User.objects.all()
    projects = Project.objects.all() 
    context = { 
        'users': users, 
        'projects': projects, 
      
    }
    return render(request, 'profiles.html', context)

def profile_search(request): 
    query = request.GET['query']
    search_results = User.objects.filter(username__icontains=query).first() 
    context = { 
        'picture': search_results, 
        'query': query,
    }
    try: 
        return redirect(reverse('profile_show', args=[search_results.id]))
    except: 
        return redirect('users/profiles')
   
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
    if request.method == 'GET':
        project_title = Reward.objects.filter(pk=id).first().project.title
        reward = Reward.objects.get(pk=id)
        context = {'project_title': project_title, 'reward': reward }
        return render(request, 'back.html', context)
    elif request.method == 'POST':
        reward = Reward.objects.get(pk=id)
        user = User.objects.get(pk=request.user.pk)
        Donation.objects.create(amount = reward.reward_amount, user = user , reward=reward)
        Project.objects.get(rewards__pk=id).backers.add(request.user)
        proj_id = reward.project.pk
        return redirect(reverse('project_show', args=[proj_id]))
        # Save reward and user to donations database
        # redirect to project page


def reward_create(request, id):
    form = RewardForm(request.POST)
    if form.is_valid():        
        reward = form.save(commit=False)
        project = Project.objects.get(pk=id)
        reward.project = project
        reward.save()
        return redirect(reverse('project_show', args=[id]))


def search(request):
    if request.method == 'GET':
        query = request.GET['query']
        search_results = Project.objects.filter(Q(title__icontains=query)|Q(description__icontains=query)|Q(category__icontains=query))
        context = {'projects': search_results, 'query':query}
        return render(request, 'search.html', context)