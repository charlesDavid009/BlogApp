from .views import SearchView, HomeView
from django.urls import path

urlpatterns = [
    path('search/', SearchView.as_view()),
    path('homeview/', HomeView.as_view()),
]
