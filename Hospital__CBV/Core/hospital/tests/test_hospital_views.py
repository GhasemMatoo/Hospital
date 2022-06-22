from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime
from accounts.models import User
from ..models import Person
# Create your tests here.


class TestHospitalView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(email="gsm90@gmail.com",
                                                  password="@/12345678")
        self.person_obj = Person.objects.create(name='Ghasem', family='Matoo',
                                                national_code='2130062385',
                                                id_number='2130062385',
                                                birth_date=datetime.now())

    def test_hospital_PersonHome_url_response_successful(self):
        url = reverse('hospital:person_home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(response.content).find('index'))
        self.assertTemplateUsed(template_name="index.html")

    def test_hospital_PersonDetailViews_login_response(self):
        self.client.force_login(self.user)
        url = reverse('hospital:person_detail', kwargs={"national_code": self.person_obj.national_code})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_hospital_PersonDetailViews_not_login_response(self):
        url = reverse('hospital:person_detail', kwargs={"national_code": self.person_obj.national_code})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)