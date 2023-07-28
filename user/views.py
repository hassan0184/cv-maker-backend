from .models import *
from .serializers import *
from .utils import *

from django.shortcuts import render
from django.utils.encoding import smart_bytes



from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,UpdateAPIView,DestroyAPIView


from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator







class UserRegister(ListCreateAPIView):
    
    serializer_class=UserSerializer
    def get_queryset(self):
        return User.objects.filter(is_staff="False",is_active=True)
    
    def get_permissions(self):
        
        permission_classes = [IsAdminUser] if self.request.method == 'GET' else []
        return [permission() for permission in permission_classes]
    

class LoginUser(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        
        response = super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        response.data['user'] = {
            'first_name': user.first_name,
            'last_name':user.last_name,
            'email': user.email,
            'last_login':user.last_login
        }
        return response
    
class ChangePassword(APIView):

    permission_classes=[IsAuthenticated]
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
class UserView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UserUpdationSerializer
        else:
            return UserSerializer
    
    def get(self, request, *args, **kwargs):
        user_obj = User.objects.get(id=self.request.user.id)
        serializer = self.get_serializer(user_obj) 
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, *args, **kwargs):
        user = request.user
        user.is_active=False
        user.save()
        return Response({'message': 'User deleted successfully.'})
    
class UserForgetPassword(APIView):
    

    def post(self, request):
         
        email = request.data.get("email")

        try:
            user = get_object_or_404(User, email=email)
        except Exception:
            return Response(data={'success': False, 'message': 'This email does not exist in our system'}, status=status.HTTP_404_NOT_FOUND)
        
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        current_site ="http://192.168.140.207:1234"
        absurl = f'{current_site}/{uidb64}/{token}/'
        send_forget_password_email(user.first_name,email,absurl)
        return Response({'success': 'Password Reset Email Sent', 'message': 'We have sent you an email with a link to reset your password. Please check your inbox and follow the instructions to reset your password.'}, status=status.HTTP_200_OK)


class SetNewPasswordAPIView(APIView):
    
    def patch(self, request,**kwargs):
        
        serializer=SetNewPasswordSerializer(data=request.data,context={'uid':kwargs['uidb64'],'token':kwargs['token']})
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)