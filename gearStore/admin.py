from django.contrib import admin
from gearStore.models import Category, UserProfile, Gear, Booking


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'dateAdded', 'picture')


class GearAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'colour', 'size', 'dateAdded', 'picture')


class BookingAdmin(admin.ModelAdmin):
    list_display = ('User.username', 'GearItem', 'DateToReturn')


admin.site.register(UserProfile)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Gear, GearAdmin)
admin.site.register(Booking)
