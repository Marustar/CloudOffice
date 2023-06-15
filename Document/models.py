from django.db import models
from Emp.models import Employee, Department
from django.utils import timezone

class File(models.Model):
    File_Name = models.CharField(max_length=100)
    File_Extend = models.CharField(max_length=10)

    def __str__(self):
        return self.File_Name


class Document(models.Model):
    Doc_ID = models.AutoField(primary_key=True)
    Doc_Dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    Doc_Sender = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, related_name="Doc_Sender")
    Doc_Receiver = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, related_name="Doc_Reciever")
    Doc_Title = models.CharField(max_length=50)
    Doc_Type = models.IntegerField()
    Doc_Files = models.ForeignKey(File, on_delete=models.CASCADE, null=True)
    Doc_State = models.IntegerField()
    Doc_Content = models.TextField(default="")
    Doc_Check = models.IntegerField(null=True)
    Doc_Time = models.DateTimeField(default=timezone.now)

    def Doc_Time2(self):
        dt = self.Doc_Time
        if dt.hour < 12:
            return dt.strftime('%Y년 %m월 %d일 오전 %I:%M:%S')
        else:
            return dt.strftime('%Y년 %m월 %d일 오후 %I:%M:%S')

    def __str__(self):
        return self.Doc_Title
