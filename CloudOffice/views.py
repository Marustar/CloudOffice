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
from django.core.paginator import Paginator
from django.db.models import Q

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


        receiveDoc = Document.Document.objects.filter(
            Doc_Receiver=currentUser, Doc_Check = 1
        )
        sentDoc = Document.Document.objects.filter(Doc_Sender=currentUser, Doc_Check=2)
        receiveMail = Mail.Mail.objects.filter(Mail_Receiver = currentUser)
        waitMail = Document.Document.objects.filter(Doc_Receiver = currentUser)
        wait_document = Document.Document.objects.filter(
            Q(Doc_Sender=currentUser) | Q(Doc_Receiver=currentUser),
            Doc_Check=3
        )
        return render (request, 'index.html', {
            'receive_document' : receiveDoc,
            'sent_document': sentDoc,
            'receive_mail' : receiveMail,
            'wait_mail' : waitMail,
            'wait_document': wait_document,
            'user_name': currentUser,
            "user_Rank": currentUser.Emp_Rank,

        })
    else:
        return redirect ('login')

    
def data(request):
    if(request.user.is_authenticated):
        return render(request, 'data.html')
    else:
        return redirect ('login')

def document(request):
    if request.user.is_authenticated:
        currentUser = findUser(request)
        receiveDoc = Document.Document.objects.filter(Doc_Receiver=currentUser, Doc_Check = 1)
        paginator = Paginator(receiveDoc, 3)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        check_value = ""

        for doc in page_obj:
            if doc.Doc_Check == 1:
                check_value = "결재 대기중"
            elif doc.Doc_Check == 2:
                check_value = "반려"
            elif doc.Doc_Check == 3:
                check_value = "결재 승인"
            doc.Check_Value = check_value

        return render(request, 'document.html', {'page_obj': page_obj})
    else:
        return redirect('login')
    

def reject(request):
    if request.user.is_authenticated:
        currentUser = findUser(request)
        receiveDoc = Document.Document.objects.filter(Doc_Sender=currentUser, Doc_Check=2)
        paginator = Paginator(receiveDoc, 3)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        check_value = ""

        for doc in page_obj:
            if doc.Doc_Check == 1:
                check_value = "결재 대기중"
            elif doc.Doc_Check == 2:
                check_value = "반려"
            elif doc.Doc_Check == 3:
                check_value = "결재 승인"
            doc.Check_Value = check_value

        return render(request, 'reject_document.html', {'page_obj': page_obj})
    else:
        return redirect('login')
    

def approval(request):
    if request.user.is_authenticated:
        currentUser = findUser(request)
        receiveDoc = Document.Document.objects.filter(
            Q(Doc_Sender=currentUser) | Q(Doc_Receiver=currentUser),
            Doc_Check=3
        )
        paginator = Paginator(receiveDoc, 3)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        for doc in page_obj:
            if doc.Doc_Check == 1:
                doc.Check_Value = "결재 대기중"
            elif doc.Doc_Check == 2:
                doc.Check_Value = "반려"
            elif doc.Doc_Check == 3:
                doc.Check_Value = "결재 승인"

        return render(request, 'approval_document.html', {'page_obj': page_obj})
    else:
        return redirect('login')
    
def viewer(request, Doc_ID):
    if(request.user.is_authenticated):
        document = get_object_or_404(Document.Document, Doc_ID = Doc_ID)
        check_value = ""
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
            
        rerank = document.Doc_Receiver.Emp_Rank
        if(rerank == 1):
            rerank = "사원"
        elif(rerank == 2):
            rerank = "대리"
        elif(rerank == 3):
            rerank = "과장"
        elif(rerank == 4):
            rerank = "차장"
        elif(rerank == 5):
            rerank = "부장"
        elif(rerank == 6):
            rerank = "사장"

        if request.method == "POST":
            doc_check = request.POST.get("Doc_Check")

            document.Doc_Check = doc_check
            document.save()


            if document.Doc_Check == 1:
                check_value = "결재 대기중"
            elif document.Doc_Check == 2:
                check_value = "반려"
            elif document.Doc_Check == 3:
                check_value = "결재 완료"

            return redirect('authenticated_home')

        if document.Doc_Check == 1:
            check_value = "결재 대기중"
        elif document.Doc_Check == 2:
            check_value = "반려"
        elif document.Doc_Check == 3:
            check_value = "결재 완료"

        print(check_value)
        return render(request, 'viewer.html', {"Document": document, "Rank": rank, "ReRank": rerank, "Check_value": check_value})
    
    else:
        return redirect('login')
    



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




