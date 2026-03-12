from django.http import HttpResponse
import django
from django.shortcuts import render

from courses.models import Category
from courses.serializers import CategorySerializer
from rest_framework import permissions
from rest_framework.filters import SearchFilter
# Create your views here.

def index(request):
    return render(request, "login.html")


from django.shortcuts import redirect
from django.conf import settings
from urllib.parse import urlencode
from rest_framework import viewsets

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_permissions(self):
        if self.request.method in ['post','put','patch']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    