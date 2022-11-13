from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

import numpy as np
import pandas as pd
import sklearn

import requests
import pickle

# To suppress the warnings
import warnings
warnings.filterwarnings('ignore')

# Custom Functions
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
    print(request.POST)

    if city != None:
        temperature, humidity = weather_fetch(city)

        with open('app/Machine-learning/Models/Crop-Recommendation/NBClassifier.pkl', 'rb') as files:
            model = pickle.load(files)
        
        data = np.array([[int(nitrogen), int(phosphorus), int(potassium), temperature, humidity, int(ph), float(rainfall)]])
        
        result = model.predict(data)
    else:
        pass
    
    return render(request, 'crop-prediction.html', context={
            'result': result[0]
        })