from django.test import TestCase
from django.urls import reverse, resolve
from hospital.views import (PersonViews, PersonDetailViews, PersonHomeViews)
# Create your tests here.


class TestHospitalUrls(TestCase):

    def test_person_home_urls_resolve(self):
        url = reverse('hospital:person_home')
        self.assertEquals(resolve(url).func.view_class, PersonHomeViews)

    def test_person_urls_resolve(self):
        url = reverse('hospital:person')
        self.assertEquals(resolve(url).func.view_class, PersonViews)

    def test_person_detail_urls_resolve(self):
        url = reverse('hospital:person_detail', kwargs={'national_code': '2130062385'})
        self.assertEquals(resolve(url).func.view_class, PersonDetailViews)