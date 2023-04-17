from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os
from django.http import HttpResponse
import comtypes.client


def viewer(request):
    return render(request, 'viewer.html')


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

        # Set the Content-Security-Policy header to allow displaying the PDF file within an iframe
        response['Content-Security-Policy'] = "frame-ancestors 'self';"

        return response
    else:
        return HttpResponse(status=404)


def ppt_to_pdf(input_path, output_path):
    comtypes.CoInitialize()
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.Visible = 1
    presentation = powerpoint.Presentations.Open(input_path)
    presentation.SaveAs(output_path, 32)  # 32 is the PDF file format
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
