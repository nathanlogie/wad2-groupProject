import django
import os
import random
from groupProject.wsgi import *

from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'groupProject.settings')

django.setup()
from gearStore.models import Gear, Booking, UserProfile, Category


def populate():
    gear = [
        {'name': 'Climbing Rope', 'description': 'A strong, dynamic rope used for climbing', 'colour': 'blue',
         'size': 'medium', 'category': 'Rope', 'picture': '/gear_images/rope.jpg'},
        {'name': 'Climbing Harnesses', 'description': 'A safety harness worn by climbers', 'colour': 'black',
         'size': 'medium', 'category': 'Harnesses', 'picture': '/gear_images/harness.jpg'},
        {'name': 'Climbing Helmet', 'description': 'A protective helmet worn by climbers', 'colour': 'green',
         'size': 'large', 'category': 'Clothing', 'picture': '/gear_images/helmet.jpg'},
        {'name': 'Climbing Shoes', 'description': 'Specialized shoes used for rock climbing', 'colour': 'green',
         'size': 'medium', 'category': 'Clothing', 'picture': '/gear_images/shoes.jpg'},
        {'name': 'Climbing Chalk Bag', 'description': 'A bag used to hold chalk for climbing', 'colour': 'red',
         'size': 'small', 'category': 'Accessories', 'picture': '/gear_images/chalkbag.jpg'},
        {'name': 'Crampons', 'description': 'Spiky attachments for climbing shoes', 'colour': 'black', 'size': 'small',
         'category': 'Accessories', 'picture': '/gear_images/g12.jpg'},
        {'name': 'Steel Ice Axe', 'description': 'A tool used for ice climbing and mountaineering', 'colour': 'blue',
         'size': 'large', 'category': 'Axes', 'picture': '/gear_images/petzl.jpeg'},
        {'name': 'Raven Ice Axe', 'description': 'A tool used for ice climbing and mountaineering', 'colour': 'black',
         'size': 'large', 'category': 'Axes', 'picture': '/gear_images/raven.png'},
        {'name': 'Mountaineering Boots', 'description': 'Boots designed for use in mountaineering', 'colour': 'green',
         'size': 'large', 'category': 'Clothing', 'picture': '/gear_images/b2.jpg'},
        {'name': 'Backpack', 'description': 'A bag for carrying gear', 'colour': 'blue',
         'size': 'medium', 'category': 'Backpacks', 'picture': '/gear_images/default.png'},
        {'name': 'Rucksack', 'description': ' A rucksack for carrying gear', 'colour': 'black', 'size': 'small',
         'category': 'Backpacks', 'picture': '/gear_images/tempest30.jpg'},
        {'name': 'Belay Device', 'description': 'A device used to control a climbing rope', 'colour': 'red',
         'size': 'small', 'category': 'Accessories', 'picture': '/gear_images/bigair.jpg'},
        {'name': 'Hiking Boots', 'description': 'Boots designed for use in hiking', 'colour': 'black', 'size': 'medium',
         'category': 'Clothing', 'picture': '/gear_images/summer.png'}
    ]

    categories = [
        {'name': 'Rope', 'description': 'Ropes for mountaineering', 'picture': '/category_images/ropes.jpg'},
        {'name': 'Harnesses', 'description': 'Harnesses for mountaineering', 'picture': '/category_images/harness.jpg'},
        {'name': 'Accessories', 'description': 'Misc accessories for mountaineering', 'picture': '/category_images/chalkbag.jpg'},
        {'name': 'Backpacks', 'description': 'Backpacks for mountaineering', 'picture': '/category_images/bag.jpg'},
        {'name': 'Axes', 'description': 'Ice axes for mountaineering', 'picture': '/category_images/axes.jpg'},
        {'name': 'Clothing', 'description': 'Clothing items for mountaineering', 'picture': '/category_images/helmet.jpg'}
    ]

    users = []

    for i in range(5):
        innerUser = User.objects.get_or_create(
            username=f'user{i}{i * 3}{i - 1}',
            email=f'user{i}@gearstore.com',
            password='password'
        )[0]
        user = UserProfile.objects.get_or_create(
            user=innerUser
        )[0]
        user.save()
        users.append(user)

    categorydict = {}

    for category in categories:
        c = Category.objects.get_or_create(
            name=category['name'],
            description=category['description'],
            picture=category['picture']
        )[0]
        c.save()
        categorydict[category['name']] = c

    gearList = []

    for gearItem in gear:
        g = Gear.objects.get_or_create(
            name=gearItem['name'],
            category=categorydict[gearItem['category']],
            description=gearItem['description'],
            colour=gearItem['colour'],
            size=gearItem['size'],
            picture = gearItem['picture']
        )[0]
        gearList.append(g)
        g.save()

    for i in range(5):
        b = Booking.objects.get_or_create(
            user=random.choice(users),
            gearItem=gearList.pop(random.randrange(len(gearList)))
        )[0]
        b.save()


if __name__ == '__main__':
    print('starting population script')
    populate()
    print('Done!')
