from django.urls import path
from .views import LoginView, RegisterView, pending_registrations
from Emp.views import pending_registrations, approve_user
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path('pending_registrations/', pending_registrations, name='pending_registrations'),
    path('approve_user/<int:user_id>/', approve_user, name='approve_user'),    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]

