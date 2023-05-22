from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    Dept_ID = models.IntegerField(primary_key=True)
    Dept_Name = models.CharField(max_length = 20)

    def __str__(self):
        return self.Dept_Name

class Employee (models.Model):
    Emp_User = models.ForeignKey(User, on_delete = models.CASCADE)
    Emp_Name = models.CharField(max_length = 10)
    Emp_Rank = models.IntegerField(null=True)
    Emp_Dept = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    is_approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.Emp_User.is_active = self.is_approved
        self.Emp_User.save()
        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return self.Emp_Name


