from django.contrib import admin
from gearStore.models import Category, UserProfile
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Category)