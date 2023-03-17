from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from gearStore.forms import UserForm, UserProfileForm
from gearStore.models import UserProfile, Category, Gear, Booking, AdminPassword
from gearStore.forms import UserForm, UserProfileForm


# Create your views here.
def index(request):
    context_dict = {}
    context_dict['boldmessage'] = 'This is the Bold Message'
    if request.user.is_authenticated:
        context_dict["user_profile"] = UserProfile.objects.get(user=request.user)
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
    return render(request, 'gearStore/category.html', context_dict)

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = UserProfile()
            profile.user = user
            profile.save()
            registered = True
        else:
            print("")
            print(user_form.errors)
    else:
        user_form = UserForm()

    if registered:
        return render(request, 'gearStore/login.html')

    else:
        errorList = []
        for error_category in user_form.errors:
            for error in user_form.errors[error_category]:
                errorList.append(error)

        return render(request, 'gearStore/register.html', context={'user_form':user_form, 'registered':registered, 'errors':errorList})

def login_page(request):
    errorList = []
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('gearStore:index'))
            else:
                errorList.append("Account has been disabled due to inactivity. Please create a new account.")
        else:
            print(f"Invalid login details: {username}, {password}")
            errorList.append("Invalid combination of user and password.")
        return render(request, 'gearStore/login.html', context={'errors':errorList})
    else:
        return render(request, 'gearStore/login.html')

def about(request):
    return render(request, 'gearStore/about.html')

def contact(request):
    return render(request, 'gearStore/contact.html')

def category_menu(request):
    context_dict = {}
    context_dict['categories'] = Category.objects.all()
    return render(request, 'gearStore/category_menu.html', context_dict)

def view_gear(request, gear_name_slug):
    context_dict = {}
    try:
        gear = Gear.objects.get(slug = gear_name_slug)
        context_dict['gear'] = gear
        current_borrow = False
        # borrows = Booking.objects.filter(gear_name_slug == gear.slug)
        # for borrow in borrows:
        #     if borrow.dateToReturn > timezone.now() and borrow.gearItem == gear.name:
        #         current_borrow = True
        #         break
        context_dict['borrowed'] = current_borrow
    except Gear.DoesNotExist:
        context_dict['gear'] = None
    return render(request, 'gearStore/view_gear.html', context_dict)

@login_required
def account(request):
    context_dict = {}
    user_profile = UserProfile.objects.get(user = request.user)
    context_dict['user_profile'] = user_profile
    if request.method == "Post":
        password = request.post.get("")

    return render(request, 'gearStore/account.html', context_dict)

@login_required
def process_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('gearStore:index'))

def admin_error(request):
    return render(request, 'gearStore/admin_error.html')

@login_required
def add_gear(request):
    return render(request, 'gearStore/add_gear.html')

@login_required
def add_category(request):
    return render(request, 'gearStore/add_category.html')
def view_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)

        gear = Gear.objects.filter(category=category)
        context_dict['gear'] = gear
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'gearStore/category.html', context=context_dict)
