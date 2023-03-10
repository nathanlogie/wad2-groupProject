from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from models import UserProfile, Category, Gear


# Create your views here.
def index(request):
    context_dict = {}
    context_dict['boldmessage'] = 'This is the Blod Message'
    if request.user.is_authenticated():
        context_dict["user_profile"] = UserProfile.objects.get(user = request.user)
    else:
        context_dict["user_profile"] = None
    context_dict["categories"] = Category.objects.all()
    return render(request, 'gearStore/index.html', context_dict)

def view_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug = category_name_slug)
    except Category.DoesNotExist:
        #Redirect to home page if category doesn't exist
        return redirect(reverse("gearStore:index"))
    context_dict["category"] = category
    context_dict["gear_list"] = Gear.object.filter(category = category)
    return render(request, 'gearStore/view_category.html', context_dict)

def about(request):
    return render(request, 'gearStore/about.html')

