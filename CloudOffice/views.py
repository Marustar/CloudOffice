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
from Emp.models import Employee
from Document.forms import DocumentForm

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
        doc_type = request.GET.get("doc_type")

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

        if doc_type:
            receiveDoc = receiveDoc.filter(Doc_Type = doc_type)

        check_value = ""

        for doc in page_obj:
            if doc.Doc_Check == 1:
                check_value = "결재 대기중"
            elif doc.Doc_Check == 2:
                check_value = "반려"
            elif doc.Doc_Check == 3:
                check_value = "결재 승인"
            doc.Check_Value = check_value


            if doc.Doc_Type == 1:
                doc.Doc_Type_String = "품의서"
            elif doc.Doc_Type == 2:
                doc.Doc_Type_String = "지출결의서"
            elif doc.Doc_Type == 3:
                doc.Doc_Type_String = "세금계산서"
            elif doc.Doc_Type == 4:
                doc.Doc_Type_String = "전표"
            elif doc.Doc_Type == 5:
                doc.Doc_Type_String = "기안서"
            elif doc.Doc_Type == 6:
                doc.Doc_Type_String = "제안서"
            elif doc.Doc_Type == 7:
                doc.Doc_Type_String = "보고서"
                

        return render(request, 'document.html', {
            'page_obj': page_obj,
            'user_name': currentUser,
            "user_Rank": currentUser.Emp_Rank,
            
            })
    else:
        return redirect('login')
    

def reject(request):
    if request.user.is_authenticated:
        currentUser = findUser(request)
        receiveDoc = Document.Document.objects.filter(Doc_Sender=currentUser, Doc_Check=2)
        paginator = Paginator(receiveDoc, 3)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        doc_type = request.GET.get("doc_type")

        if doc_type:
            receiveDoc = receiveDoc.filter(Doc_Type = doc_type)

        check_value = ""

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

        for doc in page_obj:
            if doc.Doc_Check == 1:
                check_value = "결재 대기중"
            elif doc.Doc_Check == 2:
                check_value = "반려"
            elif doc.Doc_Check == 3:
                check_value = "결재 승인"
            doc.Check_Value = check_value

            if doc.Doc_Type == 1:
                doc.Doc_Type_String = "품의서"
            elif doc.Doc_Type == 2:
                doc.Doc_Type_String = "지출결의서"
            elif doc.Doc_Type == 3:
                doc.Doc_Type_String = "세금계산서"
            elif doc.Doc_Type == 4:
                doc.Doc_Type_String = "전표"
            elif doc.Doc_Type == 5:
                doc.Doc_Type_String = "기안서"
            elif doc.Doc_Type == 6:
                doc.Doc_Type_String = "제안서"
            elif doc.Doc_Type == 7:
                doc.Doc_Type_String = "보고서"

        return render(request, 'reject_document.html', {'page_obj': page_obj, 'user_name': currentUser,
            "user_Rank": currentUser.Emp_Rank,})
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
        doc_type = request.GET.get("doc_type")

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

        if doc_type:
            receiveDoc = receiveDoc.filter(Doc_Type = doc_type)

        for doc in page_obj:
            if doc.Doc_Check == 1:
                doc.Check_Value = "결재 대기중"
            elif doc.Doc_Check == 2:
                doc.Check_Value = "반려"
            elif doc.Doc_Check == 3:
                doc.Check_Value = "결재 승인"

            if doc.Doc_Type == 1:
                doc.Doc_Type_String = "품의서"
            elif doc.Doc_Type == 2:
                doc.Doc_Type_String = "지출결의서"
            elif doc.Doc_Type == 3:
                doc.Doc_Type_String = "세금계산서"
            elif doc.Doc_Type == 4:
                doc.Doc_Type_String = "전표"
            elif doc.Doc_Type == 5:
                doc.Doc_Type_String = "기안서"
            elif doc.Doc_Type == 6:
                doc.Doc_Type_String = "제안서"
            elif doc.Doc_Type == 7:
                doc.Doc_Type_String = "보고서"

        return render(request, 'approval_document.html', {'page_obj': page_obj, 'user_name': currentUser,
            "user_Rank": currentUser.Emp_Rank,})
    else:
        return redirect('login')
    
def viewer(request, Doc_ID):
    if(request.user.is_authenticated):
        
        user = request.user
        form = DocumentForm
        try:
            employee = Employee.objects.get(Emp_User=user)
        except Employee.DoesNotExist:
            return render(request, 'fileupload.html', {'form': form})
        currentUser = findUser(request)
        rank_dict = {1: "사원", 2: "대리", 3: "과장", 4: "차장", 5: "부장", 6: "사장"}
        receiver_Rank = [ # 수신자 직급 표시
        {
            'pk': employee.pk,
            'Emp_Name': employee.Emp_Name,
            'Rank': rank_dict.get(employee.Emp_Rank, ""),
        }
        
        for employee in Employee.objects.all()
    ]
        
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
        
        current_rank = rank_dict.get(currentUser.Emp_Rank, "")
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
            
        print(rank)
            
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
        
        doc_type = document.Doc_Type


    
        if doc_type == 1:
           doc_type = "품의서"
        elif doc_type == 2:
            doc_type = "지출결의서"
        elif doc_type == 3:
            doc_type = "세금계산서"
        elif doc_type == 4:
            doc_type = "전표"
        elif doc_type == 5:
            doc_type = "기안서"
        elif doc_type == 6:
            doc_type = "제안서"
        elif doc_type == 7:
           doc_type= "보고서"




        if request.method == "POST":
            doc_check = request.POST.get("Doc_Check")
            doc_comment = request.POST.get("Doc_Comment")
            if doc_check == '4':
                document.Doc_Check =3
                print((request.POST.get('Doc_Receiver')))
                tuser = Employee.objects.get(id = request.POST.get('Doc_Receiver'))
                
                newDoc = Document.Document.objects.create(Doc_Title= document.Doc_Title, Doc_Type = document.Doc_Type, Doc_Sender = currentUser , Doc_Check = 1 , Doc_Time = document.Doc_Time, Doc_Dept = document.Doc_Dept, Doc_Receiver = tuser, Doc_Content = document.Doc_Content, Doc_Comment = document.Doc_Comment, Doc_State = document.Doc_State, Doc_Files = document.Doc_Files)
                
                
                newDoc.save()
                                
            else:    
                document.Doc_Check = doc_check
                document.Doc_Comment = doc_comment
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
        return render(request, 'viewer.html', {"Document": document, 'user_name': currentUser,
            "user_Rank": currentUser.Emp_Rank, "Rank": rank, "ReRank": rerank, "Check_value": check_value, 'Doc_Type': doc_type, 'form': form, 'username': employee.Emp_Name, 'employee': employee, 'receiver_Rank': receiver_Rank})
    
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

def base(request):
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


        return render (request, 'index.html', {

            'user_name': currentUser,
            "user_Rank": currentUser.Emp_Rank,

        })
    