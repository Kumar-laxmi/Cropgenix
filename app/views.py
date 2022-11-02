from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html', {})

def CropRecommendation(request):
    return render(request, 'crop-recommendation.html', {})