from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
import pandas as pd

# Create your views here.

def index(request):
    return render(request, 'ins/index.html')

# Code taken from Django's documentation tutorial and modified according to the needs
# Upload_file receives the file through request.FILE so it can be handled and used
# @request: request object
# return render of a template, or url.
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            my_file = request.FILES[list(request.FILES.keys())[0]]
            my_pd = pd.read_csv(my_file).head(10000)
            #Check rate per gender
            rate_man = fatality_per_gender(my_pd, 'M')
            rate_woman = fatality_per_gender(my_pd, 'F')
            #Counts values per Estado column
            count_categorical_values = my_pd['Estado'].value_counts()

            labels = list(set(my_pd['Estado']))
            data = count_categorical_values.values.tolist()
            
            #Calculate mean
            #Not taken into account 'Unidad de medida de edad'
            age_mean = my_pd[my_pd['Estado'] == 'Fallecido']
            age_mean = my_pd['Edad'].mean()
            
            #Calculate standard deviation
            age_std = my_pd[my_pd['Estado'] == 'Fallecido']
            age_std = my_pd['Edad'].std()
            
            #Top 3 highest dead cities
            #value_counts() returns the result on descending order
            highest_cities = list(my_pd['Nombre municipio'].value_counts().head(3).index)
            
            #Data to be sent to the template
            data = {
                'labels': labels, 
                'data': data, 
                'rate_man': rate_man, 
                'rate_woman': rate_woman, 
                'age_mean': age_mean,
                'age_std': age_std,
                'highest_cities': highest_cities,
            }
            
            return render(request, 'ins/dashboard.html', data)
    else:
        form = UploadFileForm()
    return render(request, 'ins/upload.html', {'form': form})

# fatality_per_gender calculates the fatality rate of the given gender and dataframe
# @my_pd: pandas dataframe containing Sexo and Estado indexes
# @gender: one letter string (aka char) which can be M or F
# return percentage: returns the rate, it means the fraction between the dead cases and the existing cases.

def fatality_per_gender(my_pd, gender):
    gender = my_pd[['Sexo', 'Estado']]
    dead = gender.loc[gender['Estado']=='Fallecido']
    percentage = dead.shape[0]/gender.shape[0]
    
    #print(f'CHECK HERE {gender}')
    #print(f'CHECK HERE {dead}')
    #print(f'CHECK HERE {percentage}')
    return percentage