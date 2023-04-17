from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Department(models.Model):
    Dept_ID = models.IntegerField(primary_key=True)
    Dept_Name = models.CharField(max_length = 20)

class Employee (models.Model):
    User_User = models.ForeignKey(User, on_delete = models.CASCADE)
    User_Name = models.CharField(max_length = 10)
    User_Rank = models.IntegerField()
    User_Dept = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)



