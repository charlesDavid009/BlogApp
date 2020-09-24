from django.urls import path, include
from profiles import views


urlpatterns = [
    path('Profile/create', views.CraeteProfileView.as_view()),
    path('Profile/<int:pk>/detail', views.UpdateProfileView.as_view()),
    path('Profile/<int:pk>/user', views.MyProfileView.as_view()),
    path('Profile/', views.GetUserView.as_view()),
    path('Profile/<int:id>/followers', views.UserFollowersView.as_view()),
    path('Profile/<int:id>/following', views.UsersFollowingView.as_view()),
    path('Profile/action', views.ProfileActionView.as_view()),
]
