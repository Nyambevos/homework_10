from django.urls import path
from . import views

app_name = 'quoteapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('author/', views.author, name='author'),
    path('tag/', views.tag, name='tag'),
    path('quote/', views.quote, name='quote'),
    path('author/<slug:slug_author>/', views.detail_author, name='detail_author'),
    path('tag/<str:tag>/', views.quotes_by_tag, name='quotes_by_tag'),
]
