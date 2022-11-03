from django.shortcuts import render

import numpy as np
import pandas as pd
import sklearn

# To load models
import pickle


# Create your views here.

def index(request):
    return render(request, 'index.html', {})

def CropRecommendation(request):
    return render(request, 'crop-recommendation.html', {})

def CropRecommendationResult(request):
    return render(request, 'crop-recommendation-result.html', {})