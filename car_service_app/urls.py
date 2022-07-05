from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views

urlpatterns = [
    path('login/', obtain_auth_token),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('listing/<int:pk>/', views.listing, name='listing'),
    path('addservice/', views.add_service, name='add_service'),
    path('serviceissuedetail/<str:token>/', views.service_issue_detail, name='service_issue')
]