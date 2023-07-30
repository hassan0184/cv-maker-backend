from .views import *

from django.contrib import admin
from django.urls import path,include



urlpatterns = [

path('dashboard/',DashboardView.as_view() ,name="dashboard"),
path('create/cv/',DashboardView.as_view() ,name="create-cv"),
path('delete/cv/',DashboardRelatedView.as_view() ,name="delete-cv"),
path('update/cv/<int:pk>/',DashboardRelatedView.as_view() ,name="update-cv"),

]
