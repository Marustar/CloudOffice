from django.contrib import admin
from .models import Document, File

# Register your models here.

admin.site.register(File)
admin.site.register(Document)