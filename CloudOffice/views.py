from django.shortcuts import render, redirect
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

def home(request):
    if(request.user.is_authenticated):
        return redirect ('authenticated_home')
    else:
        return redirect ('login')

def index(request):
    if(request.user.is_authenticated):        
        currentUser = Emp.Employee.objects.get(Emp_User = request.user)
        receiveDoc = Document.Document.objects.filter(Doc_Receiver = currentUser)
        receiveMail = Mail.Mail.objects.filter(Mail_Receiver = currentUser)
        waitMail = Document.Document.objects.filter(Doc_Receiver = currentUser)
        return render (request, 'index.html', {
            'receive_document' : receiveDoc,
            'receive_mail' : receiveMail,
            'wait_mail' : waitMail,
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
    
def viewer(request):
    if(request.user.is_authenticated):
        return render(request, 'viewer.html')
    else:
        return redirect ('login')

    
def popup(request):
    return render(request, 'popup.html')


def pdfView(request):
    pdf_path = os.path.join(settings.BASE_DIR, 'DocumentData', 'testcase.pdf')
    ppt_path = os.path.join(settings.BASE_DIR, 'DocumentData', 'testcase.pptx')

    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as f:
            pdf_file = f.read()
    else:
        if os.path.exists(ppt_path):
            ppt_to_pdf(ppt_path, pdf_path)
            with open(pdf_path, 'rb') as f:
                pdf_file = f.read()
        else:
            pdf_file = None

    if pdf_file is not None:
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="myfile.pdf"'

        response['Content-Security-Policy'] = "frame-ancestors 'self';"

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


class SendEmailView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'send_email.html')

    def post(self, request, *args, **kwargs):
        try:
            msg = MIMEMultipart()
            message = request.POST.get('message')
            password = request.POST.get('password')
            msg['From'] = request.POST.get('from_email')
            msg['To'] = request.POST.get('to_email')
            msg['Subject'] = request.POST.get('subject')
            
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com: 587')
            
            server.starttls()
            
            server.login(msg['From'], password)
            
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            
            server.quit()
            
            return HttpResponse("Successfully sent email")
        
        except Exception as e:
            return HttpResponse("Failed to send email. Error: " + str(e))