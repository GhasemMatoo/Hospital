from django.test import TestCase
from datetime import datetime
from ..forms import PersonForm, PhoneForm
from ..models import Person
# Create your tests here.


class TestHospitalForm(TestCase):

    def test_hospital_person_form_valid_data(self):
        data = {
            'name': 'Ghasem',
            'family': 'Matoo',
            'national_code': '2130062385',
            'id_number': '2130062385',
            'birth_date': datetime.now()
        }
        form = PersonForm(data)
        self.assertTrue(form.is_valid())

    def test_hospital_person_form_not_valid_data(self):
        data = {
            'family': 'Matoo',
            'national_code': '2130062385',
            'id_number': '2130062385',
            'birth_date': datetime.now()
        }
        form = PersonForm(data)
        self.assertFalse(form.is_valid())

    def test_hospital_phone_form_valid_data(self):
        person_obj = Person.objects.create(name='Ghasem', family='Matoo',
                                           national_code='2130062385',
                                           id_number='2130062385',
                                           birth_date=datetime.now())
        form = PhoneForm(data={
            'phone_number': '09119163658',
            'Person': person_obj
        })
        self.assertTrue(form.is_valid())