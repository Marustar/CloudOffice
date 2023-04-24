"""CloudOffice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from CloudOffice import views
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('approval.html', views.approval, name='approval'),
    path('data.html', views.data, name='data'),
    path('document.html', views.document, name='document'),
    path('index.html', views.home, name='home'),
    path('mail.html', views.mail, name='mail'),
    path('sent.html', views.sent, name='sent'),
    path('server.html', views.server, name='server'),
    path('signin.html', views.signin, name='signin'),
    path('signup.html', views.signup, name='signup'),
    path('sns.html', views.sns, name='sns'),
    path('popup.html', views.popup, name='popup'),

    path('admin/', admin.site.urls),
    path('viewer/', views.viewer, name='viewer'),
    path('pdf/', views.pdfView, name='pdfView'),
    path('api/auth/', include('authentication.urls')),
    path('testcase/', views.upload_document, name='upload_document'),

    path('auth/', include('authentication.urls')),
]
