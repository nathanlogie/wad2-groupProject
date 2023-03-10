from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    context_dict = {'boldmessage': 'This is the Blod Message'}
    return render(request, 'gearStore/index.html', context=context_dict)

def about(request):
    return render(request, 'gearStore/about.html')

