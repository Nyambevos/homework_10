from django.urls import path
from . import views

app_name = 'parser'

urlpatterns = [
    path('', views.main, name='main'),
    path('start/', views.run_spider, name='run'),
]