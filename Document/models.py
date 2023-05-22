from django.db import models
from Emp.models import Employee, Department

# Create your models here.

class File(models.Model):
    File_Name = models.CharField(max_length = 100)
    File_Extend = models.CharField(max_length = 10)

class Document(models.Model):
    Doc_ID = models.IntegerField(primary_key=True)
    Doc_Dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    Doc_Sender = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name="Doc_Sender")
    Doc_Receiver = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name="Doc_Reciever")
    Doc_Title = models.CharField(max_length = 50)
    Doc_Type = models.IntegerField()
    Doc_Files = models.ForeignKey(File, on_delete=models.CASCADE, null = True)
    Doc_State = models.IntegerField()
