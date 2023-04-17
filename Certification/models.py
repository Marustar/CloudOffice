from django.db import models
from Emp.models import Employee
from Document.models import Document
from django.utils import timezone

# Create your models here.
class Certification(models.Model):
    Cert_User_ID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Cert_Path = models.CharField(max_length=100)

class CertLog(models.Model):
    CLog_Time = models.DateField(default=timezone.now())
    CLog_User = models.ForeignKey(Employee, on_delete=models.CASCADE)
    CLog_Docs = models.ForeignKey(Document, on_delete = models.CASCADE)
    