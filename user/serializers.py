import re
from .models import *
from .utils import *
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed




class UserSerializer(serializers.ModelSerializer):

   confirm_password = serializers.CharField(write_only=True)
   
   class Meta:
        model=User
        fields=["first_name","last_name","email","date_joined", "password","confirm_password"]
        extra_kwargs = {
            'password': {'write_only': True}, 
        }
   def validate(self, attrs):
        
      password = attrs.get('password')
      confirm_password = attrs.pop('confirm_password')

      if password and confirm_password and password != confirm_password:
          raise serializers.ValidationError({
              'Error': "Passwords do not match."
          })
      try:
         validate_password(password)
      except ValueError as e:
         raise serializers.ValidationError({'Error': str(e)}) from e
      
      return attrs
      

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not authenticate(email=user.email, password=value):
            raise serializers.ValidationError("Incorrect old password.")
        return value
    
    def validate(self, attrs):
       
       old_password = attrs.get('old_password')
       new_password = attrs.get('new_password')
       special_characters = r'[!@#$%^&*()\-_=+{}\[\]|;:"<>,.?/]'
       special_characters_count = len(re.findall(special_characters, new_password))
       
       if old_password == new_password:
           raise serializers.ValidationError({
                 'Error': "New password must be different from the old password."
              })
       elif len(new_password) < 8:
         raise serializers.ValidationError({'Error':"Password must be at least 8 characters long."})
       
       elif special_characters_count < 1:
         raise serializers.ValidationError({'Error':"Password must contain at least 1 special character."})
       
       return attrs


class UserUpdationSerializer(serializers.ModelSerializer):

   class Meta:
        model=User
        fields=["first_name","last_name"]
        

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
  

    def validate(self, attrs):   
        password = attrs.get('password')
        token = self.context['token']
        uidb64 =self.context['uid']
        id = force_str(urlsafe_base64_decode(uidb64))
        
        try:
                user = get_object_or_404(User, id=id)
        except Exception:
                return Response(data={'success': False, 'message': 'This email does not exist in our system'}, status=status.HTTP_404_NOT_FOUND)
        
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise AuthenticationFailed('The reset link is invalid', 401)
        
        user.set_password(password)
        user.save()
        return user