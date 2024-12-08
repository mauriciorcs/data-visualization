from django.urls import path
# from . import views

from .views import DashboardMapView


urlpatterns = [
    #path('', views.chart, name='chart'),
    #path('', views.dashboard, name='dashboard')
    #path('dashboard-map/', DashboardMapView.as_view(), name='dashboard_map'),
    path('dashboard-map/', DashboardMapView.as_view(template_name='core/dashboard_map.html'), name='dashboard-map')

]