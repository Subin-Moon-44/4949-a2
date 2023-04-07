# pages/views.py
from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings
from django.views.generic import TemplateView
import pickle
import pandas as pd


def homePageView(request):
    return render(request, 'home.html')


def homePost(request):
    age = -999
    weight = -999
    height = -999
    children = -999
    smoker = ""

    try:
        # Extract value from request object by control name
        age = int(request.POST['age'])
        weight = int(request.POST['weight'])
        height = int(request.POST['height'])
        children = int(request.POST['children'])
        smoker = request.POST['smoker']
    except:
        return render(request, 'home.html', {'errorMessage': '*** The data submitted is invalid. Please try again.'})

    else:
        return HttpResponseRedirect(reverse('results', kwargs={'age': age, 'weight': weight, 'height': height, 'children': children, 'smoker': smoker}))


def dataReportView(request):
    return render(request, 'data_report.html')


def results(request, age, weight, height, children, smoker):
    print("*** Inside results()")
    # load saved model
    model_path = settings.BASE_DIR/'model_pkl_standard_scaler'
    with open(model_path, 'rb') as f:
        loaded_model = pickle.load(f)

    bmi = round(weight / ((height/100) ** 2), 3)
    smoker = 1 if smoker == "Yes" else 0
    print("***bmi: " + str(bmi))
    print("***smoker: " + str(smoker))

    single_sample_df = pd.DataFrame({'age': age, 'bmi': bmi, 'children': children, 'smoker': smoker}, index=[0])
    single_pred = loaded_model.predict(single_sample_df)
    print("Single prediction: " + str(single_pred))

    if single_pred[0] == 1:
        result = "Claimed"
    else:
        result = "Not Claimed"

    return render(request, 'results.html', {'age': age, 'weight': weight, 'height': height, 'bmi': bmi, 'children': children, 'smoker': smoker, 'pred': result})
