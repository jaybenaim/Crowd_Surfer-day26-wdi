from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .forms import *
from .models import *


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


def profile(request, id):
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
    if request.method == 'GET':
        project_title = Reward.objects.filter(pk=id).first().project.title
        reward = Reward.objects.get(pk=id)
        context = {'project_title': project_title, 'reward': reward }
        return render(request, 'back.html', context)
    elif request.method == 'POST':
        reward = Reward.objects.get(pk=id)
        user = User.objects.get(pk=request.user.pk)
        Donation.objects.create(amount = reward.reward_amount, user = user , reward=reward)
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


