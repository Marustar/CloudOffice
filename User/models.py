from django.db import models

# Create your models here.

class Departments(models.Model):
    Dept_ID = models.IntegerField(primary_key=True)
    Dept_Name = models.CharField(max_length = 20)

class Users (models.Model):
    User_ID = models.IntegerField(primary_key=True)
    User_Email = models.CharField(max_length = 50)
    User_Password = models.CharField(max_length = 64)
    User_Name = models.CharField(max_length = 10)
    User_Rank = models.IntegerField()
    User_Dept = models.ForeignKey(Departments, on_delete=models.SET_NULL, null=True)



