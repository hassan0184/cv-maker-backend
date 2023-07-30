from django.contrib import admin
from nested_admin import NestedModelAdmin, NestedInlineModelAdmin, NestedStackedInline, NestedTabularInline
from .models import *



class EducationInline(NestedTabularInline):
    model = Education
    extra = 1
    classes = ['collapse']

class ExperienceInline(NestedTabularInline):
    model = Experience
    extra = 1
    classes = ['collapse']   

class CertificationInline(NestedTabularInline):
    model = Certification
    extra = 1
    classes = ['collapse']

class ProjectInline(NestedTabularInline):
    model = Project
    extra = 1
    classes = ['collapse']
    

class SkillsInline(NestedTabularInline):
    model = Skills
    extra = 1
    classes = ['collapse']


class CvAdmin(NestedModelAdmin):
    list_display = ('id', 'user', 'created_at')

    classes = ['collapse']
    inlines = [
        EducationInline,
        SkillsInline,
        ExperienceInline,
        CertificationInline,
        ProjectInline
    ]



admin.site.register(CV, CvAdmin)
