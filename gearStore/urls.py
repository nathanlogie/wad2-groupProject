from django.urls import path
from gearStore import views

app_name = 'gearStore'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register, name='register'),
    path('contact/', views.contact, name='contact'),
    path('gear/', views.gear, name='gear'),
    path('account/', views.account, name='account')
]