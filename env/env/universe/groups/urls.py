from django.urls import path, include
from groups import views


urlpatterns = [
    path('Group/create', views.GroupCreateView.as_view()),
    path('Group/<int:pk>/detail', views.GroupRUdView.as_view()),
    path('Group/<int:id>/followers', views.GroupFollowerView.as_view()),
    path('Group/<int:id>/requests', views.GroupRequestView.as_view()),
    path('Group/<int:id>/admins', views.GroupAdminUserView.as_view()),
    path('Group/<int:id>/users', views.GroupUserView.as_view()),
    path('Group/', views.GroupListView.as_view()),
    path('Group/action', views.GroupActionView.as_view()),
    path('Group/admins_action', views.GroupAdminActionView.as_view()),
    path('Group/owner_action', views.GroupOwnerActionView.as_view()),



    #Comment Urls


    #SubComment Urls


]
