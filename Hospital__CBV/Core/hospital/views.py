from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from .models import Person, Phone, PatientStatus
from .forms import PersonForm, PhoneForm
from django.db import transaction
from itertools import chain
import pandas as pd
# Create your views here.


class PersonHomeViews(ListView):
    context_object_name = 'persons'
    template_name = 'hospital/index.html'
    paginate_by = 15

    def get_queryset(self):
        # if self.request.GET:
        if len(self.request.GET) != 0:
            if self.request.GET.get('PatientStatus_id') or self.request.GET.get('doctor_name') or\
                    self.request.GET.get('type_disease') or self.request.GET.get('hosp_time') or \
                    self.request.GET.get('name') or self.request.GET.get('family') or\
                    self.request.GET.get('national_code') != '':
                patient = PatientStatus.objects.filter(
                    Person__name__icontains=self.request.GET.get('name'),
                    Person__family__icontains=self.request.GET.get('family'),
                    Person__national_code__icontains=str(self.request.GET.get('national_code')),
                    id__icontains=self.request.GET.get('PatientStatus_id'),
                    doctor_name__icontains=self.request.GET.get('doctor_name'),
                    hosp_time__icontains=self.request.GET.get('hosp_time'),
                    type_disease__icontains=str(self.request.GET.get('type_disease'))
                )
                return patient

        fields = Person.objects.filter(name='')
        return fields


class PersonViews(ListView):

    context_object_name = 'persons'
    template_name = 'hospital/person.html'
    paginate_by = 15

    def get_queryset(self):
        person = Person.objects.all().order_by("-update_date")
        return person


class PersonDetailViews(LoginRequiredMixin, DetailView):

    template_name = 'hospital/update_person.html'
    model = Person
    slug_field = 'national_code'
    slug_url_kwarg = 'national_code'

    def post(self, request, **kwargs):
        if 'add_phone' in request.POST:
            person = Person.objects.get(national_code=str(request.path).split("/")[3])
            if not Phone.objects.filter(phone_number=request.POST['new_phone']):
                Phone.objects.get_or_create(phone_number=request.POST['new_phone'], Person=person)
            return self.get(request, **kwargs)

        elif 'register' in request.POST:
            person = Person.objects.get(national_code=str(request.path).split("/")[3])
            person.name = request.POST['name']
            person.family = request.POST['family']
            person.id_number = request.POST['id_number']
            person.birth_date = request.POST['birth_date']
            if not Person.objects.filter(national_code=request.POST['national_code']):
                person.national_code = request.POST['national_code']
            person.save()
            person = Person.objects.get(national_code=request.POST['national_code'])
            phones_boox = set(Phone.objects.filter(Person_id=person.id).values_list('phone_number', flat=True))
            request_phone_list = set(request.POST.getlist('phone'))
            phones_box = phones_boox.difference(request_phone_list)
            request_phone_list = request_phone_list.difference(phones_boox)
            # fixme: must be refactor
            for tel in range(len(phones_box)):
                phones = Phone.objects.get(phone_number=list(phones_box)[tel])
                phones.phone_number = list(request_phone_list)[tel]
                phones.save()

            return self.get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['phones_box'] = Phone.objects.filter(Person_id=kwargs.get('object').id)
        context['patient_status'] = PatientStatus.objects.filter(Person_id=kwargs.get('object').id)
        return context


class PersonDeleteViews(DetailView):
    template_name = 'hospital/person.html'
    model = Person
    slug_field = 'national_code'
    slug_url_kwarg = 'national_code'

    def get(self, request, **kwargs):
        del_person = Person.objects.get(national_code=kwargs.get('national_code'))
        for phone in Phone.objects.filter(Person_id=del_person.id):
            Phone.objects.get(id=phone.id).delete()
        del_person.delete()
        return redirect('/person/')


class PersonFormViews(ListView):
    template_name = 'hospital/person_form.html'
    model = Person
    context_object_name = 'persons'

    def post(self, request, **kwargs):
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
                                Phone.objects.get_or_create(phone_number=phone, Person=person)
                return redirect('/person/forms/')
            context = {'form_person': form_person, 'form_phone': form_phone, 'phones_box': phones_box}
            return render(request, self.template_name, context)

    def get(self, request, **kwargs):
        form_person = PersonForm()
        form_phone = PhoneForm()
        context = {'form_person': form_person, 'form_phone': form_phone}
        return render(request, self.template_name, context)


class PersonUploadExcelViews(View):
    template_name = 'hospital/upload_excel.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, **kwargs):
        data_excel = (request.FILES["upload_file"])
        df = pd.read_excel(data_excel)
        standard_nan_row = df
        person_list = []
        if 'NATIONAL_CODE' in df.columns:
            for i in range(len(standard_nan_row)):
                name = standard_nan_row.loc[i]['FIRST_NAME']
                family = standard_nan_row.loc[i]['LAST_NAME']
                national_code = standard_nan_row.loc[i]['NATIONAL_CODE']
                birth_date = standard_nan_row.loc[i]['BIRTH_DATE'].replace(" 00:00:00", "")
                if not national_code == '-' and national_code.isnumeric():
                     if not Person.objects.filter(national_code=national_code):
                        person = Person(name=name, family=family, national_code=national_code, birth_date=birth_date)
                        person_list.append(person)
            Person.objects.bulk_create(person_list)
        else:
            messages.add_message(request, messages.WARNING, 'invalid excl file.')
        return render(request, self.template_name)


class PatientStatusDetailViews(LoginRequiredMixin, DetailView):

    template_name = 'hospital/update_patient.html'
    model = PatientStatus
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Patient'] = PatientStatus.objects.filter(Person_id=kwargs.get('object').id)
        return context