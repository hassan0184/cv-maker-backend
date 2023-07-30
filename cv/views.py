from .models import *
from .serializers import *

from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404


from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated


class DashboardView(ListCreateAPIView):

    permission_classes=[IsAuthenticated]
    serializer_class=DashboardSerializer
    
    def get_queryset(self):
        return CV.objects.filter(user=self.request.user)
    
    def get_serializer_context(self):
        return {"user":self.request.user}
    

class DashboardRelatedView(RetrieveUpdateDestroyAPIView):

    permission_classes=[IsAuthenticated]
    serializer_class=DashboardSerializer

    def delete(self, request, *args, **kwargs):
        cv_obj=CV.objects.filter(user=self.request.user)
        if cv_obj.exists():
            cv_obj.delete()
            response_data = {
                'message': 'CV deleted successfully.',
            }
        else:
            response_data = {
                'message': 'No CV found for deletion. Nothing was deleted.',
            }
        return JsonResponse(response_data)
    
    
    def get_queryset(self):
        return CV.objects.filter(user=self.request.user)
    

    def get_serializer_context(self):
        return {"user":self.request.user}
   


