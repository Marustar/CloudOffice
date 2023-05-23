from django.db import models
from Emp.models import Employee
from Document.models import File, Document


# Create your models here.
class Mail(models.Model):
    Mail_ID = models.IntegerField(primary_key=True)
    Mail_Sender = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='Mail_Sender')
    Mail_Receiver = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='Mail_Reciever')
    Mail_Title = models.CharField(max_length = 50)
    Mail_contents = models.CharField(max_length = 500)
    Mail_Create_Time = models.DateTimeField(auto_now=True)
    Mail_Isread = models.BooleanField(default=False)
    Mail_Files = models.ForeignKey(File, on_delete=models.SET_NULL, null=True, default=None)
    Mail_Docs = models.ForeignKey(Document, on_delete=models.SET_NULL, null = True, default=None)

    def __str__(self):
        return self.Mail_Title