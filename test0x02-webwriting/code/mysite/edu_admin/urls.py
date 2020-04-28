from django.urls import path
from .views import *

urlpatterns = [
     path('index/<int:pk>', index),
     path('myscore', my_score),
]
