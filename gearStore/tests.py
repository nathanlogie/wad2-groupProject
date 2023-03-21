import datetime
import unittest

from django.contrib.auth.models import User
from django.test import TestCase
from django.template.defaultfilters import slugify
from django.urls import reverse

import gearStore.forms
import populate_gearStore
from gearStore.forms import CategoryForm, GearForm, UserProfileForm, AdminForm
from gearStore.models import UserProfile, Category, Gear, Booking, AdminPassword


class ModelTests(TestCase):
    def createUserprofile(self):
        return UserProfile.objects.create(
            user=User.objects.create_user(
                username="TestCaseUser",
                email="Tester@yahoo.com",
                password="password"),
            adminStatus=False)

    def testUserProfile(self):
        prof = self.createUserprofile()
        self.assertTrue(isinstance(prof, UserProfile))
        self.assertEqual(prof.__str__(), "TestCaseUser")
        self.assertTrue(isinstance(prof.user, User))

    def createCategory(self):
        category = Category.objects.create(
            name="TestCategory",
            description="TestingCategory"
        )
        return category

    def testCategory(self):
        cat = self.createCategory()
        self.assertTrue(isinstance(cat, Category))
        self.assertEqual(cat.__str__(), "TestCategory")
        self.assertEqual(cat.slug, slugify(cat.name))

    def createGear(self):
        gear = Gear.objects.create(
            category=self.createCategory(),
            name="TestGear",
            description="TestingGear",
            colour="GREEN",
            size="SMALL"
        )
        return gear

    def testGear(self):
        gear = self.createGear()
        self.assertTrue(isinstance(gear, Gear))
        self.assertTrue(isinstance(gear.category, Category))
        self.assertEqual(gear.__str__(), "TestGear")
        self.assertEqual(gear.dateAdded, datetime.date.today())

    def createBooking(self):
        return Booking.objects.create(user=self.createUserprofile(), gearItem=self.createGear())

    def testBooking(self):
        booking = self.createBooking()
        self.assertTrue(isinstance(booking, Booking))
        self.assertEqual(booking.__str__(), "TestCaseUser booking of TestGear")
        self.assertTrue(isinstance(booking.user, UserProfile))
        self.assertTrue(isinstance(booking.gearItem, Gear))


class FormTests(TestCase):

    def test_add_category_form(self):
        self.assertTrue('CategoryForm' in dir(gearStore.forms))
        form = CategoryForm()
        self.assertEqual(type(form.__dict__['instance']), Category)

    def test_add_gear_form(self):
        self.assertTrue('GearForm' in dir(gearStore.forms))
        form = GearForm()
        self.assertEqual(type(form.__dict__['instance']), Gear)

    def test_add_userprofile(self):
        self.assertTrue('UserProfileForm' in dir(gearStore.forms))
        form = UserProfileForm()
        self.assertEqual(type(form.__dict__['instance']), UserProfile)

    def test_admin(self):
        self.assertTrue('AdminForm' in dir(gearStore.forms))
        form = AdminForm()
        self.assertEqual(type(form.__dict__['instance']), AdminPassword)


class TestPopulateScript(TestCase):

    def testAdded(self):
        populate_gearStore.populate()
        cats = Category.objects.all()
        gear = Gear.objects.all()
        booking = Booking.objects.all()
        self.assertTrue(len(cats) > 1)
        self.assertTrue(len(gear) > 1)
        self.assertTrue(len(booking) > 1)


class ViewTests(TestCase):

    def testAbout(self):
        url = reverse("gearStore:about")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "gearStore/about.html")

    def testRedirect(self):
        url = reverse("gearStore:add-category")
        self.client.logout()
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, "/gear-store/login/?next=/gear-store/add-category/")

    def testLoggedIn(self):
        model = ModelTests()
        user = model.createUserprofile()
        self.client.force_login(user=user.user)
        url = reverse("gearStore:add-category")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def testRedirectStatus(self):
        url = reverse("gearStore:add-category")
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def testMissingdata(self):
        model = ModelTests()
        user = model.createUserprofile()
        self.client.force_login(user=user.user)

        url = reverse('gearStore:add-category')
        data = {'name': '',
                'description': 'TestDescriptioning'}

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', 'This field is required.')

    @unittest.expectedFailure
    def testAutofillView(self):
        model = ModelTests()
        user = model.createUserprofile()
        self.client.force_login(user=user.user)

        url = reverse('gearStore:add-category')
        data = {'name': '',
                'description': 'TestDescriptioning'}

        response = self.client.post(url, data=data)
        self.assertFormError(response, 'form', 'description', 'This field is required.')
        self.assertFormError(response, 'form', 'picture', 'This field is required.')
