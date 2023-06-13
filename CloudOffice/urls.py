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
from Document.models import Document
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('approval.html', views.approval, name='approval'),
    path('data.html', views.data, name='data'),
    path('document.html', views.document, name='document'),
    path('index.html', views.index, name='authenticated_home'),
    path('viewer.html/<int:Doc_ID>/', views.viewer, name='viewer'),
    path('admin/', admin.site.urls),
    
    path('pdf/<int:Doc_ID>/', views.pdfView, name='pdfView'),
    path('api/auth/', include('authentication.urls')),
    # path('testcase/', views.upload_document, name='upload_document'),

    path('auth/', include('authentication.urls')),
    #path('send-email/', SendEmailView.as_view(), name='send-email'),
    path('upload/', include('Document.urls')),  # 'Document' is the name of your app
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
