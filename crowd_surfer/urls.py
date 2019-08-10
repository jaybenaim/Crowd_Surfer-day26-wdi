from django.contrib import admin
from django.urls import path, include 
from .views import *


urlpatterns = [
    path('', root), 
    path('admin/', admin.site.urls),
    path('home/', home),
    path('accounts/signup', signup, name='signup'), 
    path('accounts/signup_create', signup_create, name='signup_create'), 
    path('accounts/profile/', include('django.contrib.auth.urls')), 
    path('users/<int:id>/profile', profile_show, name='profile_show'),
    path('users/profiles', profiles, name='profiles'),
    path('projects/create', project_create, name='project_create'),
    path('projects/<int:id>', project_show, name='project_show'),
    path('projects/<int:id>/rewards/create', reward_create, name="reward_create"),
    path('rewards/<int:id>/back', back_project, name='back_project'),
   
]