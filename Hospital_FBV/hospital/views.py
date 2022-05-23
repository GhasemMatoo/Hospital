from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from hospital.models import Phone, Person
from .forms import PersonForm, PhoneForm
import pandas as pd
# Create your views here.


def home_views(request, **kwargs):
    if request.GET:
        person = Person.objects.filter(
            name__icontains=request.GET.get('name'),
            family__icontains=request.GET.get('family'),
            national_code__icontains=str(request.GET.get('national_code')))
        if kwargs.get('national_code'):
            del_person = Person.objects.get(national_code=kwargs.get('national_code'))
            for phone in Phone.objects.filter(Person_id=del_person.id):
                Phone.objects.get(id=phone.id).delete()
            del_person.delete()
            return redirect('/')
        paginator = Paginator(person, 16)
        page_number = request.GET.get('page')
        persons = paginator.get_page(page_number)
        context = {'persons': persons}
        return render(request, 'mysit/index.html', context)
    return render(request, 'mysit/index.html')


def person_views(request, **kwargs):
    persons = Person.objects.all().order_by("-update_date")
    paginator = Paginator(persons, 16)
    page_number = request.GET.get('page')
    persons = paginator.get_page(page_number)
    if kwargs.get('national_code'):
        del_person = Person.objects.get(national_code=kwargs.get('national_code'))
        for phone in Phone.objects.filter(Person_id=del_person.id):
            Phone.objects.get(id=phone.id).delete()
        del_person.delete()
        return redirect('/person')
    context = {'persons': persons}
    return render(request, 'mysit/person.html', context)


def person_form_views(request):
    phones_box = []
    if request.method == 'POST':
        form_person = PersonForm(request.POST)
        form_phone = PhoneForm(request.POST)
        request_list = request.POST.getlist('phones') + [request.POST['phone_number']]
        phones_box = request_list
        if 'register' in request.POST:
            if form_person.is_valid():
                person = form_person.save(commit=False)
                with transaction.atomic():
                    person.save()
                    for phone in request_list:
                        if not Phone.objects.filter(phone_number=phone):
                            Phone.objects.get_or_create(phone_number=phone,Person=person)

           # else:
                #messages.add_message(request, messages.WARNING, 'This number has already been used.')
    else:
        form_phone = PhoneForm()
        form_person = PersonForm()
    context = {'form_person': form_person, 'form_phone': form_phone, 'phones_box': phones_box}
    return render(request, 'mysit/person_form.html', context)


def person_update_views(request, **kwargs):
    if request.method == 'GET':
        if kwargs.get('national_code'):
            person = Person.objects.get(national_code=kwargs.get('national_code'))
            phones_box = Phone.objects.filter(Person_id=person.id)
            '''
            TODO
            json_data = json.dumps({person})
            '''
        context = {'person': person, 'phones_box':phones_box}
    if request.method == 'POST':
        if kwargs.get('national_code'):
            person = Person.objects.get(national_code=kwargs.get('national_code'))
            phones_box = Phone.objects.filter(Person_id=person.id)
            if 'add_phone' in request.POST:
                new_phone = request.POST['new_phone']
                if not Phone.objects.filter(phone_number=new_phone):
                    Phone.objects.get_or_create(phone_number=new_phone, Person=person)
                '''
                TODO == msg use phone number
                '''
            if 'register' in request.POST:
                person.name = request.POST['name']
                person.family = request.POST['family']
                person.id_number = request.POST['id_number']
                person.birth_date = request.POST['birth_date']
                if not Person.objects.filter(national_code=request.POST['national_code']):
                    person.national_code = request.POST['national_code']
                person.save()
                person = Person.objects.get(national_code=kwargs.get('national_code'))
                phones_box = Phone.objects.filter(Person_id=person.id)
                request_phone_list = request.POST.getlist('phone')
                for tel in range(len(request_phone_list)):
                    if len(phones_box) > tel:
                        if not str(phones_box[tel]) == request_phone_list[tel]:
                            print(phones_box[tel],"==",request_phone_list[tel])
                            phones_box[tel].phone_number = request_phone_list[tel]
                            phones_box[tel].save()
    form_phone = PhoneForm()
    form_person = PersonForm()
    context = {'person': person, 'phones_box': phones_box,'form_person': form_person, 'form_phone': form_phone}
    return render(request, 'mysit/update_person.html', context)


def person_upload_excel_views(request):
    if request.method == 'POST':
        data_excel = (request.FILES["upload_file"])
        df = pd.read_excel(data_excel)
        standard_nan_row =df
        if 'NATIONAL_CODE' in df.columns:
            for i in range(len(standard_nan_row)):
                name = standard_nan_row.loc[i]['FIRST_NAME']
                family = standard_nan_row.loc[i]['LAST_NAME']
                national_code = standard_nan_row.loc[i]['NATIONAL_CODE']
                birth_date = standard_nan_row.loc[i]['BIRTH_DATE'].replace(" 00:00:00", "")
                if not national_code == '-':
                    if not Person.objects.filter(national_code=national_code):
                        Person.objects.get_or_create(name=name,family=family,national_code=national_code,birth_date=birth_date)
        else:
            messages.add_message(request, messages.WARNING, 'invalid excl file.')
    return render(request, 'mysit/upload_excel.html',)