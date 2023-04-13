from django.db import models
from ..User.models import Users, Departments

# Create your models here.

class Files(models.Model):
    File_Name = models.CharField(max_length = 100)
    File_Extend = models.CharField(max_length = 10)

class Documents(models.Model):
    Doc_ID = models.IntegerField(primary_key=True)
    Doc_Dept = models.ForeignKey(Departments, on_delete=models.CASCADE)
    Doc_Sender = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    Doc_Reciever = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    Doc_Title = models.CharField(max_length = 50)
    Doc_Type = models.IntegerField()
    Doc_Files = models.ForeignKey(Files, on_delete=models.CASCADE, null = True)
    Doc_State = models.IntegerField()
