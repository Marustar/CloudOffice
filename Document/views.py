from django.shortcuts import render, redirect
from .models import Document, File
from .forms import DocumentForm
from Emp.models import Employee, Department
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.conf import settings
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
