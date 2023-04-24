from django.contrib import admin
from .models import Certification, CertLog

# Register your models here.

admin.site.register(Certification)
admin.site.register(CertLog)