from django.test import TestCase
from datetime import datetime
from ..models import Person
# Create your tests here.


class TestHospitalModel(TestCase):

    def test_create_person(self):
        person_obj = Person.objects.create(name='Ghasem', family='Matoo',
                                           national_code='2130062385',
                                           id_number='2130062385',
                                           birth_date=datetime.now())
        self.assertEqual(person_obj.name, 'Ghasem')
        self.assertTrue(Person.objects.filter(national_code=person_obj.national_code).exists())