from django import forms
from .models import Document, File
from Emp.models import Department, Employee


class DocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        departments = Department.objects.all()
        choices = [(dept.Dept_ID, dept.Dept_Name) for dept in departments]
        self.fields['Doc_Dept'].choices = choices

    class Meta:
        model = Document
        fields = ['Doc_ID', 'Doc_Dept', 'Doc_Title', 'Doc_Sender',
                  'Doc_Receiver', 'Doc_Type', 'Doc_State', 'Doc_Content', 'Doc_Check']
