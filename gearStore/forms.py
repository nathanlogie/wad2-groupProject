import django.utils.timezone
from django import forms
from django.contrib.auth.models import User

from gearStore.models import UserProfile, Category, COLOUR_CHOICES, SIZE_CHOICES, Gear


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please the enter the category name.")
    description = forms.CharField(max_length=128)
    dateAdded = forms.DateField(widget=forms.HiddenInput(), required=False)
    picture = forms.ImageField(required=False)
    slug = forms.SlugField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)


class GearForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please the enter the gear name.")
    description = forms.CharField(max_length=128)
    dateAdded = forms.DateField(widget=forms.HiddenInput(), required=False)
    picture = forms.ImageField(required=False)
    colour = forms.ChoiceField(choices=COLOUR_CHOICES)
    size = forms.ChoiceField(choices=SIZE_CHOICES)
    slug = forms.SlugField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Gear
        exclude = ('category',)
