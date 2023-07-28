from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display=['id','email','first_name','last_name','date_joined','is_active','is_staff']

admin.site.register(User,UserAdmin)
