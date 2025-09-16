from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Welcome to College Fest!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),  # include app urls
]