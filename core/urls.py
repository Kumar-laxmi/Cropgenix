"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from app.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', index),
    path('crop-recommendation/', CropRecommendation),
    path('crop-prediction/<str:nitrogen>/<str:phosphorus>/<str:potassium>/<str:ph>/<str:rainfall>/<str:state>/<str:city>/', CropRecommendationResult),
    path('fertilizer-recommendation/', FertilizerRecommendation),
    path('fertilizer-prediction/<str:temperature>/<str:humidity>/<str:moisture>/<str:soil>/<str:crop>/<str:nitrogen>/<str:potassium>/<str:phosphorus>/', FertilizerRecommendationResult)
]
