from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os
from django.http import HttpResponse


def pdfView(request):
    # PDF 파일 경로
    pdf_path = os.path.join(settings.BASE_DIR, 'DocumentData', 'testcase.pdf')

    # PDF 파일 열기
    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as f:
            pdf_file = f.read()
    else:
        pdf_file = None

    # PDF 파일을 HttpResponse 객체에 담아 반환
    if pdf_file is not None:
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="myfile.pdf"'
        return response
    else:
        return HttpResponse(status=404)