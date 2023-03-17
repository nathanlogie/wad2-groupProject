from datetime import timedelta

import django.utils.timezone
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=128)
    dateAdded = models.DateField(auto_now_add=True)
    picture = models.ImageField(upload_to="category_images", default="category_images/default.png")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    adminStatus = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='profile_images', default="profile_images/default.jpeg")

    def __str__(self):
        return self.user.username


COLOUR_CHOICES = (
    ('green', 'GREEN'),
    ('blue', 'BLUE'),
    ('red', 'RED'),
    ('orange', 'ORANGE'),
    ('black', 'BLACK'),
)

SIZE_CHOICES = (
    ('small', 'SMALL'),
    ('medium', 'MEDIUM'),
    ('large', 'LARGE'),

)


class Gear(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    dateAdded = models.DateField(auto_now_add=True)
    picture = models.ImageField(default="gear_images/default.png")
    colour = models.CharField(max_length=6, choices=COLOUR_CHOICES, default="GREEN")
    size = models.CharField(max_length=30, choices=SIZE_CHOICES, default="SMALL")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Gear"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Gear, self).save(*args, **kwargs)


def return_date_time():
    now = timezone.now()
    return now + timedelta(days=7)


class Booking(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    gearItem = models.ForeignKey(Gear, on_delete=models.CASCADE)
    dateBorrowed = models.DateField(auto_now_add=True)
    dateToReturn = models.DateField(default=return_date_time)

    def __str__(self):
        return f"{self.user.user.username} booking of {self.gearItem.name}"

class AdminPassword(models.Model):
    password = models.CharField(max_length=64, default="password123")