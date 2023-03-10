from django.urls import path
from gearStore import views

app_name = 'gearStore'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
]