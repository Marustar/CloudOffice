from django.urls import path
from .views import LoginView, RegisterView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),  
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]

