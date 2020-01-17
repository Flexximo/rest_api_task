from django.urls import path, re_path
from .views import api_handler

urlpatterns = [    
    path('cars/', api_handler, name="manager"),
    re_path(r'cars/(?P<id>[A-Za-z0-9]{8})', api_handler, name="editor"),
]