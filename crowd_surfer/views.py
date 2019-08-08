from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .forms import *
# from .models import *


def root(request): 
    return redirect('home/')
    
def home(request): 
    return render(request, 'index.html')
    
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
    context = {'project': Project.objects.get(pk=id)}
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

def back_project(request, id):
    return redirect(reverse('project_create', args=['article.id']))
    pass 



