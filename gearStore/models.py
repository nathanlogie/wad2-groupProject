import datetime

import django.utils.timezone
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=128)
    dateAdded = models.DateTimeField(default=django.utils.timezone.now())
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
