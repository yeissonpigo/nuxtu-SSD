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
            
            #Gets pie chart values
            pie_values = get_categorical(my_pd, 'Estado')
            
            #Calculate mean
            #Not taken into account 'Unidad de medida de edad'
            mean = get_mean(my_pd, 'Estado', 'Edad', 'Fallecido')
            
            #Calculate standard deviation
            std = get_std(my_pd, 'Estado', 'Edad', 'Fallecido')
            
            #Top 3 highest dead cities
            #value_counts() returns the result on descending order
            highest_cities = list(my_pd['Nombre municipio'].value_counts().head(3).index)
            lowest_cities = list(my_pd['Nombre municipio'].value_counts().tail(3).index)
            
            #Data to be sent to the template
            data = {
                'pie_values': pie_values,
                'rate_man': rate_man, 
                'rate_woman': rate_woman, 
                'mean': mean,
                'std': std,
                'highest_cities': highest_cities,
                'lowest_cities': lowest_cities,
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
    
    return percentage

# get_categorical get the categorical values of a given column index, and calculates how many times the value appears on the dataframe
# @my_pd: pandas dataframe containing Sexo and Estado indexes
# @column_name: string which must match a column name from @my_pd
# return result: returns a list, with the labels and values for a pie chart in chart.js

def get_categorical(my_pd, column_name):
    count_categorical_values = my_pd[column_name].value_counts()
    labels = list(set(my_pd['Estado']))
    labels = [x for x in labels if str(x) != 'nan']
    data = count_categorical_values.values.tolist()
    result = [labels, data]
    print(count_categorical_values)
    return result

# get_mean calculates the mean of a given column name from a given dataframe, of a given categorical value
# @my_pd: pandas dataframe containing Sexo and Estado indexes
# @column_filter: string which must match a column name from @my_pd to be filtered
# @column_mean: string which must match a column name from @my_pd to calculate mean
# @value_filter: string which must match a categorical value from @column_filter
# return mean: returns the mean value

def get_mean(my_pd, column_filter, column_mean, value_filter):
    my_pd[my_pd[column_filter] == value_filter]
    mean = my_pd[column_mean].mean()
    return mean

# get_std calculates the standard deviation of a given column name from a given dataframe, of a given categorical value
# @my_pd: pandas dataframe containing Sexo and Estado indexes
# @column_filter: string which must match a column name from @my_pd to be filtered
# @column_mean: string which must match a column name from @my_pd to calculate mean
# @value_filter: string which must match a categorical value from @column_filter
# return std: returns the standard deviation value

def get_std(my_pd, column_filter, column_mean, value_filter):
    my_pd[my_pd[column_filter] == value_filter]
    std = my_pd[column_mean].std()
    return std

# get_mean_date calculates the mean deviation of a given column name from a given dataframe, of a given categorical value
# @my_pd: pandas dataframe containing Sexo and Estado indexes
# @column_filter: string which must match a column name from @my_pd to be filtered
# @column_mean: string which must match a column name from @my_pd to calculate mean
# @value_filter: string which must match a categorical value from @column_filter
# return std: returns the standard deviation value

def get_std(my_pd, column_filter, column_mean, value_filter):
    my_pd[my_pd[column_filter] == value_filter]
    std = my_pd[column_mean].std()
    return std