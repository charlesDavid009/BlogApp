from .views import RegisterAPI
from django.urls import path

urlpatterns = [
    path('Account/register/', RegisterAPI.as_view(), name='register'),
]
