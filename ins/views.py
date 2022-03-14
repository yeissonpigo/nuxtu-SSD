from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
import pandas as pd

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
        print(form.is_valid())
        if form.is_valid():
            my_file = request.FILES[list(request.FILES.keys())[0]]
            my_pd = pd.read_csv(my_file)
            print(f'CHECK HERE {my_pd}')
    else:
        form = UploadFileForm()
    return render(request, 'ins/upload.html', {'form': form})

def fatality_per_gender(request, my_pd):
    return 0