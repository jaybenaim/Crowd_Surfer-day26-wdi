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
]