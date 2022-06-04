from django import forms
from .models import Person, Phone

'''
create form model person and phone
'''


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'family', 'national_code', 'id_number', 'birth_date']


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ['phone_number']
