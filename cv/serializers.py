from .models import *

from rest_framework import serializers
from django.db import transaction

class EducationSerializer(serializers.ModelSerializer):

    class Meta:
        model=Education
        fields = ['institute','degree','field_of_study','description','from_year','to_year']

class skillsSerializer(serializers.ModelSerializer):

    class Meta:
        model=Skills
        fields = ['skill','description']

class ExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model=Experience
        fields = ['job_title','organization','city','country','description','start_date','end_date']

class CertificationSerializer(serializers.ModelSerializer):

    class Meta:
        model=Certification
        fields = ['name','issuing_organization','issue_date','expiration_date']


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model=Project
        fields = ['name','description','start_date','end_date']



class DashboardSerializer(serializers.ModelSerializer):
   
    educations = EducationSerializer(many=True)
    skills = skillsSerializer(many=True)
    experiences = ExperienceSerializer(many=True)
    certifications = CertificationSerializer(many=True)
    projects = ProjectSerializer(many=True)
    
    class Meta:
        model=CV
        fields=['id','objective','hobbies_and_interests','created_at','skills','educations','experiences','certifications','projects']

    def create(self, validated_data):

        with transaction.atomic():
        
            educations_data = validated_data.pop('educations')
            skills_data = validated_data.pop('skills')
            experiences_data = validated_data.pop('experiences')
            certifications_data = validated_data.pop('certifications')
            projects_data = validated_data.pop('projects')

            user = self.context.get('user')
            if CV.objects.filter(user=user).exists():
                raise serializers.ValidationError("You can create only one CV with the free plan.")

            cv = CV.objects.create(user=user, **validated_data)

            for education_data in educations_data:
                Education.objects.create(cv=cv, **education_data)

            for skill_data in skills_data:
                Skills.objects.create(cv=cv, **skill_data)

            for experience_data in experiences_data:
                Experience.objects.create(cv=cv, **experience_data)

            for certification_data in certifications_data:
                Certification.objects.create(cv=cv, **certification_data)

            for project_data in projects_data:
                Project.objects.create(cv=cv, **project_data)

            return cv