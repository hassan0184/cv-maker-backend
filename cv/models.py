from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField
from user.models import *
import datetime

class CV(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cvs')
    objective = models.TextField(max_length=400)
    hobbies_and_interests = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)  # Add a timestamp when the CV is created

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} CV"

class Education(models.Model):
    from_year =models.DateField()
    to_year = models.DateField(null=True, blank=True) 
    institute = models.CharField(max_length=100) 
    degree = models.CharField(max_length=100, null=True, blank=True)  
    field_of_study = models.CharField(max_length=100, null=True, blank=True)  
    description = models.TextField(max_length=300, null=True, blank=True)  
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='educations')

    def __str__(self):
        return f"{self.from_year}-{self.to_year}: {self.institute}"

class Experience(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True) 
    job_title = models.CharField(max_length=128)
    organization = models.CharField(max_length=100, null=True, blank=True)  
    city = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=600, null=True, blank=True)  
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='experiences')

    def __str__(self):
        return f"{self.job_title} at {self.organization or 'Unknown Organization'}"


class Certification(models.Model):
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True) 
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='certifications')

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=400)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.name
    

class Skills(models.Model):
    skill=models.CharField(max_length=50, null=True)
    description=models.TextField(max_length=300,null=True,blank=True)
    cv=models.ForeignKey(CV,on_delete=models.CASCADE, related_name='skills')

    class Meta:
        verbose_name_plural="skills"





