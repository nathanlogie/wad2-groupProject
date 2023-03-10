from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from gearStore.models import UserProfile, Category
#from gearStore.forms import UserForm, UserProfileForm


# Create your views here.
def index(request):
    context_dict = {}
    context_dict['boldmessage'] = 'This is the Blod Message'
    if request.user.is_authenticated:
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

def register(request):
    return render(request, 'gearStore/register.html')
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit = False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'gearStore/register.html', context={'user_form':user_form, 'profile_form':profile_form, 'registered':registered})

def login(request):
    return render(request, 'gearStore/login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('gearStore:index'))
            else:
                return HttpResponse("Your Gear Store account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request, 'gearStore/login.html')

def about(request):
    return render(request, 'gearStore/about.html')

def contact(request):
    return render(request, 'gearStore/contact.html')