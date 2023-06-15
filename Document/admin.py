from django.contrib import admin
from .models import Document, File

admin.site.register(File)
admin.site.register(Document)