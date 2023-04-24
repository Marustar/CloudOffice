from django.db import models
from Emp.models import Employee
from Document.models import File

# Create your models here.
class Board(models.Model): 
    Board_ID = models.IntegerField(primary_key=True)
    Board_Writer = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    Board_Create_Time = models.DateTimeField(auto_now=True)
    Board_Title = models.CharField(max_length=50)
    Board_Content = models.TextField
    Board_Files = models.ForeignKey(File, on_delete=models.CASCADE, null = True)