from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render, redirect

from .forms import *

import numpy as np
import pandas as pd
import sklearn

import requests
import pickle

# To suppress the warnings
import warnings
warnings.filterwarnings('ignore')

# Custom Functions
# function to return key for any value
def get_key(val, my_dict):
    for key, value in my_dict.items():
        if val == value:
            return key
 
    return "key doesn't exist"

def weather_fetch(city_name):
    """
    Fetch and returns the temperature and humidity of a city
    :params: city_name
    :return: temperature, humidity
    """
    api_key = "50f9831aa5470ef6c5b200b434bf35db"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]

        temperature = round((y["temp"] - 273.15), 2)
        humidity = y["humidity"]
        return temperature, humidity
    else:
        return None


# Create your views here.

def index(request):
    return render(request, 'index.html', {})

def CropRecommendation(request):
    return render(request, 'crop-recommendation.html', {})

def CropRecommendationResult(request, nitrogen, phosphorus, potassium, ph, rainfall, state, city):
    crop_image = {
        'apple': './app/static/img/apple.jpeg',
        'banana': './app/static/img/banana.webp',
        'blackgram': './app/static/img/blackgram.jpeg',
        'chickpea': './app/static/img/chickpea.jpeg',
        'coffee': './app/static/img/coffee.jpeg',
        'cotton': './app/static/img/cotton.webp',
        'grapes': './app/static/img/grapes.jpeg',
        'jute': './app/static/img/jute.jpeg',
        'kidneybeans': './app/static/img/kidneybeans.jpeg',
        'lentil': './app/static/img/lentil.jpeg',
        'maize': './app/static/img/maize.webp',
        'mango': './app/static/img/mango.jpeg',
        'mothbeans': './app/static/img/mothbeans.jpeg',
        'mungbean': './app/static/img/mungbean.jpeg',
        'muskmelon': './app/static/img/muskmelon.jpeg',
        'orange': './app/static/img/orange.jpeg',
        'papaya': './app/static/img/papaya.jpeg',
        'pigeonpeas': './app/static/img/pigeonpeas.jpeg',
        'pomegranate': './app/static/img/pomegranate.webp',
        'rice': './app/static/img/rice.jpeg',
        'watermelon': './app/static/img/watermelon.jpeg'
    }
    if city != None:
        city = city.lstrip()
        try:
            temperature, humidity = weather_fetch(city)
        except:
            temperature, humidity = weather_fetch('Goa')

        with open('app/Machine-learning/Models/Crop-Recommendation/NBClassifier.pkl', 'rb') as files:
            model = pickle.load(files)
        
        data = np.array([[int(nitrogen), int(phosphorus), int(potassium), temperature, humidity, int(ph), float(rainfall)]])
        
        result = model.predict(data)
        result_image = crop_image[result[0]]
        print(result_image)
    else:
        pass
    
    return render(request, 'crop-prediction.html', context={
            'result': result[0],
            'result_image': result_image
        })

def FertilizerRecommendation(request):
    return render(request, 'fertilizer-recommendation.html', {})

def FertilizerRecommendationResult(request, temperature, humidity, moisture, soil, crop, nitrogen, potassium, phosphorus):
    with open('app/Machine-learning/Models/Fertilizer-Recommendation/rf_pipeline.pkl', 'rb') as files:
        model1 = pickle.load(files)

    with open('app/Machine-learning/Models/Fertilizer-Recommendation/croptype_dict.pkl', 'rb') as files:
        croptype = pickle.load(files)

    with open('app/Machine-learning/Models/Fertilizer-Recommendation/fertname_dict.pkl', 'rb') as files:
        fertilizername = pickle.load(files)

    with open('app/Machine-learning/Models/Fertilizer-Recommendation/soiltype_dict.pkl', 'rb') as files:
        soiltype = pickle.load(files)

    Soil = get_key(soil, soiltype)
    Crop = get_key(crop, croptype)

    data = np.array([[float(temperature), float(humidity), float(moisture), Soil, Crop, float(nitrogen), float(potassium), float(phosphorus)]])
    result = fertilizername[model1.predict(data)[0]]

    return render(request, 'fertilizer-prediction.html', context={
        'result': result
    })

def CropDisease(request):
    return render(request, 'crop-disease.html', {})

def image_view(request):
    if request.method == 'POST':
        form = LeafDiseaseForm(request.POST, request.FILES)
 
        if form.is_valid():
            form.save()
    else:
        form = LeafDiseaseForm()

    return render(request, 'hotel_image_form.html', {'form': form})
