from django.shortcuts import render, redirect
from .models import Document, File
from .forms import DocumentForm
from Emp.models import Employee, Department
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from docx import Document
from django.conf import settings
from docx2pdf import convert
import os
from Emp import models as Emp
import pythoncom
import comtypes.client

def findUser(request):
    return Emp.Employee.objects.get(Emp_User = request.user)
    
@login_required
def document_upload(request):
    pythoncom.CoInitialize()
    document_types = [1, 2, 3]
    user = request.user
    form = DocumentForm()  
    try:
        employee = Employee.objects.get(Emp_User=user)
    except Employee.DoesNotExist:
        return render(request, 'fileupload.html', {'form': form})  

    currentUser = findUser(request) # 발신자 직급 표시

    rank_dict = {1: "사원", 2: "대리", 3: "과장", 4: "차장", 5: "부장", 6: "사장"}
    current_rank = rank_dict.get(currentUser.Emp_Rank, "")

    receiver_Rank = [ # 수신자 직급 표시
        {
            'pk': employee.pk,
            'Emp_Name': employee.Emp_Name,
            'Rank': rank_dict.get(employee.Emp_Rank, ""),
        }
        for employee in Employee.objects.all()
    ]

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            form.instance.Doc_Dept = employee.Emp_Dept
            document = request.FILES.get('document')
            if document:
                document_name = process_file(document)
                document_path = os.path.join(settings.BASE_DIR, 'DocumentData', document_name)
                file_name = os.path.splitext(document_name)[0]
                file_extend = os.path.splitext(document_name)[1]
                file_ist = File()
                file_ist.File_Name = file_name + file_extend
                file_ist.File_Extend = file_extend
                file_ist.save()
                form.instance.Doc_Files = file_ist

            form.save()
            return redirect('/index.html')
        else:
            print(form.errors)
    else:
        form = DocumentForm()

    context = {
        'form': form,
        'username': employee.Emp_Name, 
        'Rank': current_rank,  
        'employee': employee,
        'receiver_Rank': receiver_Rank,  
        'document_types': document_types
    }

    return render(request, 'fileupload.html', context)



def convert_ppt_to_pdf(file):
    file_extension = os.path.splitext(file.name)[1].lower()

    if file_extension in ['.ppt', '.pptx']:
        document_name = file.name
        file_path = os.path.join(settings.BASE_DIR, 'DocumentData', document_name)

        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        if not os.path.isfile(file_path):
            print("파일을 찾을 수 없습니다.")
            return None

        pdf_path = file_path.replace('.pptx', '.pdf')

        powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
        powerpoint.Visible = 1

        if file_extension == '.ppt':
            ppt = powerpoint.Presentations.Open(file_path)
        else:
            ppt = powerpoint.Presentations.Open2007(file_path)
            
        ppt.ExportAsFixedFormat(pdf_path, 2)
        ppt.Close()
        powerpoint.Quit()

        os.remove(file_path)

        return os.path.basename(pdf_path)

    return None



def convert_doc_to_pdf(file):
    file_extension = os.path.splitext(file.name)[1].lower()

    if file_extension in ['.doc', '.docx']:
        document_name = file.name
        file_path = os.path.join(settings.BASE_DIR, 'DocumentData', document_name)

        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        pdf_path = file_path.replace('.docx', '.pdf')

        convert(file_path, pdf_path)

        os.remove(file_path)

        return os.path.basename(pdf_path)

    return None



def process_file(file):
    file_extension = os.path.splitext(file.name)[1].lower()

    if file_extension in ['.ppt', '.pptx']:
        return convert_ppt_to_pdf(file)
    elif file_extension in ['.doc', '.docx']:
        return convert_doc_to_pdf(file)

    return None