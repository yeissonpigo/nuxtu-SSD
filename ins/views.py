from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from .templates.ins import *

# Create your views here.

def index(request):
    return render(request, 'ins/index.html')

# Code taken from Django' documentation tutorial
# Upload_file receives the file through request.FILE so it can be handled and used
# @request: request object
# return render of a template, or url.
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #handle_uploaded_file(request.FILES['file'])
            return HttpResponse('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'ins/upload.html', {'form': form})