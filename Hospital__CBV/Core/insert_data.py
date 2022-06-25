import django
django.setup()
from hospital.models import Person
import pandas as pd


def insert():
    df = pd.read_excel("1.xls")
    standard_nan_row = df
    person_list = []
    for i in range(len(standard_nan_row)):
        name = standard_nan_row.loc[i]['FIRST_NAME']
        family = standard_nan_row.loc[i]['LAST_NAME']
        national_code = standard_nan_row.loc[i]['NATIONAL_CODE']
        birth_date = standard_nan_row.loc[i]['BIRTH_DATE'].replace(" 00:00:00", "")
        person = Person(name=name, family=family, national_code=national_code, birth_date=birth_date)
        person_list.append(person)
    Person.objects.bulk_create(person_list)


if __name__ == '__main__':
    insert()