from django.shortcuts import render, redirect
from .models import Document, File
from .forms import DocumentForm
from Emp.models import Employee, Department
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from docx import Document
from django.conf import settings
from docx2pdf import convert
import pdfkit
import os

@login_required
def document_upload(request):
    document_types = [1, 2, 3]    
    user = request.user
    try:
        employee = Employee.objects.get(Emp_User=user)
    except Employee.DoesNotExist:
        return redirect('login')

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.Doc_Dept = employee.Emp_Dept
            
            document = request.FILES.get('document')
            if document:
                document = process_file(document)
                document_name = document.name
                document_path = os.path.join(settings.BASE_DIR, 'DocumentData', document_name)
                with open(document_path, 'wb+') as destination:
                    for chunk in document.chunks():
                        destination.write(chunk)
                
                file_name = os.path.splitext(document_name)[0]
                file_extend = os.path.splitext(document_name)[1]
                
                file_ist = File()
                file_ist.File_Name = file_name
                file_ist.File_Extend = file_extend
                file_ist.save()
                form.instance.Doc_Files = file_ist
                
                response_data = {
                    'status': 'success',
                    'document_name': document.name,
                }
                
            
            form.save()
            return redirect('/document_upload?success_page=true')
        else:
            print(form.errors)
    else:
        form = DocumentForm()

    return render(request, 'fileupload.html', {'form': form, 'employee': employee, 'document_types': document_types})


def convert_ppt_to_pdf(file):
    file_extension = os.path.splitext(file.name)[1].lower()

    if file_extension == '.ppt':
        file_path = 'temp.ppt'
        with open(file_path, 'wb') as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)

        pdf_path = 'converted.pdf'
        convert(file_path, pdf_path)

        os.remove(file_path)

        with open(pdf_path, 'rb') as pdf_file:
            pdf_data = pdf_file.read()

        os.remove(pdf_path)

        return pdf_data

    return None

def convert_doc_to_pdf(file):
    file_extension = os.path.splitext(file.name)[1].lower()

    if file_extension == '.doc':
        document_name = file.name
        file_path = os.path.join(settings.BASE_DIR, 'DocumentData', document_name)

        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        pdf_path = file_path.replace('.doc', '.pdf')

        convert(file_path, pdf_path)

        with open(pdf_path, 'rb') as pdf_file:
            pdf_data = pdf_file.read()

        os.remove(file_path)
        os.remove(pdf_path)

        return pdf_data

    return None

def process_file(file):
    file_extension = os.path.splitext(file.name)[1].lower()

    if file_extension == '.ppt':
        return convert_ppt_to_pdf(file)
    elif file_extension == '.doc':
        return convert_doc_to_pdf(file)

    return None