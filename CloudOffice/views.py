from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os
import pptx


def ppt_viewer(request):
    ppt_file_path = os.path.join(settings.BASE_DIR, 'DocumentData', 'testcase.pptx')
    prs = pptx.Presentation(ppt_file_path)
    return render(request, 'viewer_ppt.html', {'slides': prs.slides})