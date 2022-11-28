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