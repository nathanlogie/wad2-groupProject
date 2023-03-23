import datetime
from datetime import *

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from gearStore.forms import UserForm, UserProfileForm, CategoryForm, GearForm, AdminForm
from gearStore.models import UserProfile, Category, Gear, Booking, AdminPassword, COLOUR_CHOICES


# Create your views here.
def index(request):
    context_dict = {'categories': Category.objects.all()}
    context_dict['categories'] = Category.objects.all()
    context_dict['category'] = None
    return render(request, 'gearStore/index.html', context_dict)


def view_category(request, category_name_slug):
    context_dict = {'categories': Category.objects.all()}
    context_dict['categories'] = Category.objects.all()
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        # Redirect to home page if category doesn't exist
        return redirect(reverse("gearStore:index"))
    context_dict["category"] = category
    context_dict["gear_list"] = Gear.object.filter(category=category)
    return render(request, 'gearStore/category.html', context=context_dict)


def register(request):
    context_dict = {'categories': Category.objects.all()}
    context_dict['category'] = None
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
        return render(request, 'gearStore/login.html', context=context_dict)

    else:
        errorList = []
        for error_category in user_form.errors:
            for error in user_form.errors[error_category]:
                errorList.append(error)
        context_dict['errors'] = errorList
        context_dict['user_form'] = user_form
        context_dict['registered'] = registered

        return render(request, 'gearStore/register.html', context=context_dict)


def login_page(request):
    context_dict = {'categories': Category.objects.all()}
    context_dict['category'] = None
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
        context_dict['errors'] = errorList
        return render(request, 'gearStore/login.html', context=context_dict)
    else:
        return render(request, 'gearStore/login.html', context=context_dict)


def about(request):
    context_dict = {'categories': Category.objects.all()}
    context_dict['category'] = None
    return render(request, 'gearStore/about.html', context_dict)


def contact(request):
    context_dict = {'categories': Category.objects.all()}
    context_dict['category'] = None
    return render(request, 'gearStore/contact.html', context_dict)


def category_menu(request):
    context_dict = {'categories': Category.objects.all()}
    context_dict['category'] = None
    return render(request, 'gearStore/category_menu.html', context_dict)


def view_gear(request, gear_name_slug):
    context_dict = {'categories': Category.objects.all()}
    try:
        gear = Gear.objects.get(slug=gear_name_slug)
        context_dict['gear'] = gear

        # attempt to borrow the gear
        if request.method == 'POST':
            borrow = Booking()
            if request.user:
                borrow.gearItem = gear
                borrow.user = UserProfile.objects.get(user=request.user)
                borrow.dateToReturn = datetime.now().date() + timedelta(days=14)
                borrow.save()

        # find if the gear is currently on loan
        current_borrow = False
        borrows = Booking.objects.filter(gearItem=gear)
        for borrow in borrows:
            if borrow.is_current():
                current_borrow = True
                context_dict["borrow"] = borrow
                break
        context_dict['borrowed'] = current_borrow

        # find the gear's category
        try:
            category = Category.objects.get(name=gear.category)
            context_dict['category'] = category
        except Category.DoesNotExist:
            context_dict['category'] = None
    except Gear.DoesNotExist:
        context_dict['gear'] = None
    return render(request, 'gearStore/view_gear.html', context_dict)


@login_required
def account(request):
    context_dict = {'categories': Category.objects.all()}
    context_dict['category'] = None
    user_profile = UserProfile.objects.get(user=request.user)
    context_dict['user_profile'] = user_profile
    passwords = AdminPassword.objects.all()
    if not passwords:
        user_profile.adminStatus = True
    password_form = AdminForm()
    picture_form = UserProfileForm()

    if request.method == "POST":
        post_type = request.POST.get("post-type")
        if post_type == "picture":
            # get new profile picture
            picture_form = UserProfileForm(request.POST or None, request.FILES, instance=user_profile)
            if picture_form.is_valid():
                picture_form.save()
        elif post_type == "password":
            password_form = AdminForm(request.POST)
            if password_form.is_valid():
                if not passwords:
                    password = password_form.save(commit=True)
                elif user_profile.adminStatus:
                    passwords[0].password = request.POST.get("password")
                    passwords[0].save()
                else:
                    if passwords[0].password == request.POST.get("password"):
                        user_profile.adminStatus = True
                        user_profile.save()
    context_dict['picture_form'] = picture_form
    context_dict['password_form'] = password_form

    user_bookings = Booking.objects.filter(user=user_profile)
    for booking in user_bookings:
        if not booking.is_current():
            user_bookings = user_bookings.exclude(id = booking.id)
    context_dict["user_bookings"] = user_bookings

    if user_profile.adminStatus:
        all_bookings = Booking.objects.all()
        for booking in all_bookings:
            if not booking.is_current():
                all_bookings = all_bookings.exclude(id = booking.id)
        context_dict["all_bookings"] = all_bookings

    return render(request, 'gearStore/account.html', context_dict)


@login_required
def process_logout(request):
    context_dict = {'categories': Category.objects.all()}
    context_dict['category'] = None
    logout(request)
    return redirect(reverse('gearStore:index'))


def admin_error(request):
    context_dict = {'categories': Category.objects.all()}
    context_dict['category'] = None
    return render(request, 'gearStore/admin_error.html', context=context_dict)


def view_category(request, category_name_slug):
    context_dict = {'categories': Category.objects.all()}
    try:
        category = Category.objects.get(slug=category_name_slug)

        gear = Gear.objects.filter(category=category)
        context_dict['gear'] = gear
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['gear'] = None
    return render(request, 'gearStore/category.html', context=context_dict)


@login_required
def add_category(request):
    errorList = []
    context_dict = {'categories': Category.objects.all()}
    form = None
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('/gear-store/')
        else:
            print(form.errors)
            for error_category in form.errors:
                for error in form.errors[error_category]:
                    errorList.append(error)
    context_dict['errors'] = errorList
    context_dict['form'] = form
    return render(request, 'gearStore/add_category.html', context_dict)


@login_required
def add_gear(request, category_name_slug):
    context_dict = {'categories': Category.objects.all()}
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect(reverse("gearStore:index"))

    form = GearForm()

    if request.method == 'POST':
        form = GearForm(request.POST, request.FILES)

        if form.is_valid():
            if category:
                gear = form.save(commit=False)
                gear.category = category
                gear.save()
                return redirect(reverse('gearStore:view-category',
                                        kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)
    context_dict['form'] = form
    context_dict['category'] = category
    return render(request, 'gearStore/add_gear.html', context=context_dict)
