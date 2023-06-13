from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render, redirect
import os
from django.http import HttpResponse
import comtypes.client
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Document import models as Document
from Mail import models as Mail
from Emp import models as Emp
from Document.models import File
from django.contrib.auth.decorators import login_required

@login_required
def findUser(request):
    return Emp.Employee.objects.get(Emp_User = request.user)


def home(request):
    if(request.user.is_authenticated):
        return redirect ('authenticated_home')
    else:
        return redirect ('login')

def index(request):
    if(request.user.is_authenticated):        
        currentUser = findUser(request)
        
        if(currentUser.Emp_Rank == 1):
            currentUser.Emp_Rank = "사원"
        elif(currentUser.Emp_Rank == 2):
            currentUser.Emp_Rank = "대리"
        elif(currentUser.Emp_Rank == 3):
            currentUser.Emp_Rank = "과장"
        elif(currentUser.Emp_Rank == 4):
            currentUser.Emp_Rank = "차장"
        elif(currentUser.Emp_Rank == 5):
            currentUser.Emp_Rank = "부장"
        elif(currentUser.Emp_Rank == 6):
            currentUser.Emp_Rank = "사장"
            

        receiveDoc = Document.Document.objects.filter(Doc_Receiver = currentUser)
        # print(receiveDoc[0].id)
        receiveMail = Mail.Mail.objects.filter(Mail_Receiver = currentUser)
        waitMail = Document.Document.objects.filter(Doc_Receiver = currentUser)
        return render (request, 'index.html', {
            'receive_document' : receiveDoc,
            'receive_mail' : receiveMail,
            'wait_mail' : waitMail,
            'user_name': currentUser,
            "user_Rank": currentUser.Emp_Rank,

        })
    else:
        return redirect ('login')

    

def approval(request):
    if(request.user.is_authenticated):
        return render(request, 'approval.html')
    else:
        return redirect ('login')
    
def data(request):
    if(request.user.is_authenticated):
        return render(request, 'data.html')
    else:
        return redirect ('login')

def document(request):
    if(request.user.is_authenticated):
        return render(request, 'document.html')
    else:
        return redirect ('login')

def mail(request):
    if(request.user.is_authenticated):
        return render(request, 'mail.html')
    else:
        return redirect ('login')

def sent(request):
    if(request.user.is_authenticated):
        return render(request, 'sent.html')
    else:
        return redirect ('login')

def server(request):
    if(request.user.is_authenticated):
        return render(request, 'server.html')
    else:
        return redirect ('login')


def sns(request):
    if(request.user.is_authenticated):
        return render(request, 'sns.html')
    else:
        return redirect ('login')
    
def viewer(request, Doc_ID):
    if(request.user.is_authenticated):
        document = get_object_or_404(Document.Document, Doc_ID = Doc_ID)
        rank = document.Doc_Sender.Emp_Rank
        if(rank == 1):
            rank = "사원"
        elif(rank == 2):
            rank = "대리"
        elif(rank == 3):
            rank = "과장"
        elif(rank == 4):
            rank = "차장"
        elif(rank == 5):
            rank = "부장"
        elif(rank == 6):
            rank = "사장"
        return render(request, 'viewer.html',{"Document":document, "Rank":rank} )
    
    else:
        return redirect ('login')
    

def popup(request):
    return render(request, 'popup.html')


# def pdfView(request, file_id):

#     file = get_object_or_404(File, id = file_id)
#     document_name = "{}{}".format(file.File_Name, file.File_Extend)

#     pdf_path = os.path.join(settings.BASE_DIR, 'DocumentData', 'document_name')

#     if os.path.exists(pdf_path):
#         with open(pdf_path, 'rb') as f:
#             pdf_file = f.read()
#     else:
#         pdf_file = None

#     if pdf_file is not None:
#         response = HttpResponse(pdf_file, content_type='application/pdf')
#         response['Content-Disposition'] = 'filename="myfile.pdf"'

#         # response['Content-Security-Policy'] = "frame-ancestors 'self';"

#         return response
#     else:
#         return HttpResponse(status=404)

def pdfView(request, Doc_ID):
    document = get_object_or_404(Document.Document, Doc_ID = Doc_ID)
    document_name = document.Doc_Files.File_Name
    pdf_path = os.path.join(settings.BASE_DIR, 'DocumentData', document_name)
    print(pdf_path)

    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as f:
            pdf_file = f.read()
    else:
        pdf_file = None

    if pdf_file is not None:
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="myfile.pdf"'

        # response['Content-Security-Policy'] = "frame-ancestors 'self';"

        return response
    else:
        return HttpResponse(status=404)


def ppt_to_pdf(input_path, output_path):
    comtypes.CoInitialize()
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.Visible = 1
    presentation = powerpoint.Presentations.Open(input_path)
    presentation.SaveAs(output_path, 32)
    presentation.Close()
    powerpoint.Quit()


def convert_ppt_to_pdf(request):
    input_path = "/path/to/input.pptx"
    output_path = "/path/to/output.pdf"
    ppt_to_pdf(input_path, output_path)
    with open(output_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=output.pdf'
        return response


def upload_document(request):
    if request.method == 'POST':
        document = request.FILES.get('document')
        if document:
            document_name = document.name
            document_path = os.path.join(settings.BASE_DIR, 'DocumentData', document_name)
            with open(document_path, 'wb+') as destination:
                for chunk in document.chunks():
                    destination.write(chunk)
            response_data = {
                'status': 'success',
                'document_name': document.name,
            }
            success_page_url = '/testcase/?success_page=true'
            return HttpResponseRedirect(success_page_url)
    return render(request, 'fileupload.html')




