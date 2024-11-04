from django.urls import path
from . import views

urlpatterns = [
    #path('', views.chart, name='chart'),
    path('', views.dashboard, name='dashboard')
    
]