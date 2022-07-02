# Config for debug and setup Django
import django
django.setup()
# import madel and library
from hospital.models import Person, PatientStatus
from faker import Faker
from random import randint
from datetime import datetime
import pandas as pd
############################
doctor_list = [
    "حسینعلی هادی", "مهران اعظمی", "حمدرضا بهروزی", "محسن پارسی", "آرشام جنگ میری", "محمدرضا بزرگمنش", "محمد یگانه شالی"
    , "محمدرضا یگانه خو", "نادر زرین فر", "حسین سرمدیان", "فرشیده دیدگر", "معصومه صوفیان", "حسین مظاهر پور", "افشین بابایی"
    , " سپیده خدر زاده ", "پژمان حدادی", " کیوان قسامی", "فردین فرجی", " محسن ابراهیمی", "محمدرضا انعامی", "لیلا پورسعادت"
    , "فاطمه محمودی", "علی فراهانی ", " سید احمد صالحی", "بهناز دانشفر", "علی غیاث آبادی", " گیلا حشمتی", " مریم کسروی ",
    "ماندانا مجیدیان ", "محسن دالوندی", "علیرضا محمدی", "علی ناظمی رفیع ", "مهدی خالقی" , "محمدباقر صادقی ",
    "علیرضا رستمی " , "عابد قاری", "ابوالفضل محترمی ", "علی داودی", "صدیقه درویش", "معصومه حیدری", "سعید حیدری",
    "مهدی وفایی " , "سپیده شیرین", "مهتاب بنیادی", "احسان رحیمی", "علیرضا رستمی", "محمدرضا غلامی","حسن سعیدی",
    "قاسم متو"
]


def insert_person():
    # Get data in to excel for create Person
    df = pd.read_csv("CMN_PERSON.csv")
    standard_nan_row = df
    person_list = []
    national_dic = {}
    for i in range(len(standard_nan_row)):
        name = standard_nan_row.loc[i]['FIRST_NAME']
        family = standard_nan_row.loc[i]['LAST_NAME']
        national_code = standard_nan_row.loc[i]['NATIONAL_CODE']
        birth_date = standard_nan_row.loc[i]['BIRTH_DATE'].replace(" 00:00:00", "")
        if national_code not in national_dic.values():
            if len(str(national_code)) == 10 and national_code.isnumeric():
                person = Person(name=name, family=family, national_code=national_code,
                                birth_date=birth_date)
                person_list.append(person)
                national_dic[i] = national_code
    Person.objects.bulk_create(person_list)


def insert_patient_status():
    # Get data in to excel for create DISEASE_PRIMARY_NAME
    start_date = datetime(year=2020, month=1, day=1)
    end_date = datetime(year=2022, month=6, day=15)
    fake = Faker()

    df = pd.read_excel("DISEASE_PRIMARY_NAME.xlsx", sheet_name="result 1")
    standard_nan_row = df
    adad = len(standard_nan_row)
    rang = int(adad / 100)
    step = rang
    start = 15
    for j in range(0, 101):
        patient_status_list = []
        for i in range(start, rang):
            if i >= adad:
                break
            type_disease = standard_nan_row.loc[i]['DISEASE_PRIMARY_NAME']
            doctor_name = doctor_list[randint(0, len(doctor_list)) - 1]
            invoice = randint(30000, 3000000)
            hosp_time = fake.date_between(start_date=start_date, end_date=end_date)
            person = randint(1, 650870)
            patient_status = PatientStatus(doctor_name=doctor_name, type_disease=type_disease,
                                           invoice=invoice, hosp_time=hosp_time, Person_id=person)
            patient_status_list.append(patient_status)
        if j < 101:
            print("step in work : %{}".format(j))
        start = rang
        rang = rang + step
        print("start to db")
        PatientStatus.objects.bulk_create(patient_status_list)
        print("END_insert_patient_status")


if __name__ == '__main__':
    insert_patient_status(),
    # insert_person(),

