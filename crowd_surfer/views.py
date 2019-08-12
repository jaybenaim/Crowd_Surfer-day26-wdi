
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
import pdb
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
    total_donations = Donation.objects.filter(reward__project__pk=id).aggregate(Sum('amount'))
    if total_donations['amount__sum'] == None:
        total_donations['amount__sum']=0
    funding_end_date = project.funding_end_date 
    delta = datetime.datetime(funding_end_date.year, funding_end_date.month, funding_end_date.day) - datetime.datetime.now()
    
    status = project_status(project)

    context = {
        'project': project,
        'form': reward_form,
        'rewards': rewards, 
        'total_donations': total_donations['amount__sum'], 
        'delta': delta,
        'comment_form': CommentForm(), 
        'comments' : Comment.objects.filter(project_id=project.id),
        'status': status
        }

    return render(request, 'project.html', context)

@login_required
def profile_show(request, id):
    projects = Project.objects.filter(owner_id=id)
    backers = Project.backers
    donations = Donation.objects.filter(reward__project__owner_id=id)
    total_donations = Donation.objects.filter(reward__project__backers=id).aggregate(Sum('amount'))
    proj_status = {}
    for project in projects:
        proj_status[project.title]=project_status(project)
    total_recieved = 0 
    for donation in donations:
        total_recieved += donation.amount 

    return render(request, 'profile.html', { 
        'projects': projects, 
        'backers': backers,
        'project_donations': donations,
        'donations': total_donations,
        'total_recieved' : total_recieved,
        'project_status': proj_status,
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
            form.save_m2m()
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


def reward_delete(request, id):
    ids = request.POST.getlist('delete_reward')
    for reward_id in ids:
        reward = Reward.objects.get(pk=reward_id)
        reward.delete()

    return redirect(reverse('project_show', args=[id]))
    
    
    
    # for reward_id in ids:
    #     print(reward_id)
    #     reward = Reward.objects.get(pk=reward_id)
    #     reward.delete()
    

@login_required 
def create_comment(request): 
    params = request.POST 
    project_id = params['project']
    project = get_object_or_404(Project, pk=project_id)

    comment = Comment() 
    comment.user = request.user
    comment.text = params['text']
    comment.project = project

    comment.save()

    return redirect(reverse('project_show', args=[project_id]))
   
@login_required    
def edit_comment(request, id):
    comment_to_edit = Comment.objects.get(pk=id)
    form = CommentForm(request.POST, instance=comment_to_edit)
    if request.method == 'GET':
        context = {'form': form, 'action': f'/comments/{id}/edit'}
        return render(request, 'form.html', context)
    else:
        form.save()
        action = f'/comments/{comment_to_edit.pk}/update'
        context = {'comment': comment_to_edit, 'form': form, "message": "Edit Comment", 'action': action}
        return redirect(reverse('project_show', args=[comment_to_edit.project.id]))


@login_required
def update_comment(request, id):
    params = request.POST 
    project_id = params['project']
    comment_to_update = Comment.objects.get(pk=id)
    form = CommentForm(instance=comment_to_update)
    form.save()
    return redirect(reverse('project_show', args=[project_id]))


@login_required
def delete_comment(request, id):
    params = request.POST 
    project_id = params['project']
    comment_to_del = Comment.objects.get(pk=id)
    comment_to_del.delete()
    return redirect(reverse('project_show', args=[project_id]))


def search(request):
    if request.method == 'GET':
        query = request.GET['query']
        search_results = Project.objects.filter(Q(title__icontains=query)|Q(description__icontains=query)|Q(category__icontains=query))
        result_categories = []
        result_tags = []
        for project in search_results:
            if project.category not in result_categories:
                result_categories.append(project.category)
            for tag in project.tags.names():
                if tag not in result_tags:
                    result_tags.append(tag)
        context = {'projects': search_results, 'query':query, 'categories': result_categories, 'tags':result_tags}
        return render(request, 'search.html', context)

def search_refine(request):
    query = request.method == 'GET'
    query = request.GET['query']
    result_categories = []
    result_tags = []
    category_list = request.GET.getlist('category_check')
    tag_list = request.GET.getlist('tag_check')
    search_results = Project.objects.filter(Q(title__icontains=query)|Q(description__icontains=query))
    if len(category_list) != 0:
        search_results = search_results.filter(category__in=category_list)
    if len(tag_list) != 0:
        search_results = search_results.filter(tags__name__in=tag_list)

    for project in search_results:
        if project.category not in result_categories:
            result_categories.append(project.category)
        for tag in project.tags.names():
            if tag not in result_tags:
                result_tags.append(tag)
    context = {'projects': search_results, 'query':query, 'categories': result_categories, 'tags':result_tags}
    return render(request, 'search.html', context)

def categories(request):
    context = {}
    categories = []
    for choice_tuple in cat_choices:
        if choice_tuple[1] != '-----':
            categories.append(choice_tuple[1])
    categories.sort()
    context['categories'] = categories
    total_projects_by_category = {}
    total_funding_by_category = {}

    for category in categories:
        num_projects_by_category = len(Project.objects.filter(category__icontains=category))
        total_projects_by_category[category] = num_projects_by_category
        num_funding_by_category = Project.objects.filter(category__icontains=category).aggregate(Sum('rewards__donations__amount'))
        if num_funding_by_category['rewards__donations__amount__sum'] == None:
            total_funding_by_category[category] = 0
        else:
            total_funding_by_category[category] = num_funding_by_category['rewards__donations__amount__sum']

    context['total_projects'] = total_projects_by_category
    context['funding'] = total_funding_by_category
    
    return render(request, 'categories.html', context)


def project_status(project):
    if project.is_funded() == True and project.is_expired() == True:
        status = 'Complete'
    elif project.is_funded()== True and project.is_expired() == False:
        status = 'Backed'
    elif project.is_funded()== False and project.is_expired() == True:
        status = 'Expired'
    else:
        status = 'Running'
    return status