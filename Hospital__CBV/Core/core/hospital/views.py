from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Person, Phone
from .forms import PersonForm, PhoneForm
from django.db import transaction
# Create your views here.


class PersonHomeViews(ListView):
    context_object_name = 'persons'
    template_name = 'hospital/index.html'
    paginate_by = 2

    def get(self, request, **kwargs):
        if len(request.GET) != 0:
            persons = Person.objects.filter(
                name__icontains=request.GET.get('name'),
                family__icontains=request.GET.get('family'),
                national_code__icontains=str(request.GET.get('national_code'))
            )
            context = {'persons': persons}
            return render(request, self.template_name, context)
        return render(request, self.template_name)


class PersonViews(ListView):

    context_object_name = 'persons'
    template_name = 'hospital/person.html'
    paginate_by = 2

    def get_queryset(self):
        person = Person.objects.all().order_by("-update_date")
        return person


class PersonDetailViews(DetailView):

    template_name = 'hospital/update_person.html'
    model = Person
    slug_field = 'national_code'
    slug_url_kwarg = 'national_code'

    def post(self, request, **kwargs):
        post_request = request.POST
        if 'add_phone' in post_request:
            person = Person.objects.get(national_code=str(request.path).split("/")[3])
            new_phone = post_request['new_phone']
            if not Phone.objects.filter(phone_number=new_phone):
                Phone.objects.get_or_create(phone_number=new_phone, Person=person)
                return self.get(request, **kwargs)
        if 'register' in post_request:
            person = Person.objects.get(national_code=str(request.path).split("/")[3])
            person.name = request.POST['name']
            person.family = request.POST['family']
            person.id_number = request.POST['id_number']
            person.birth_date = request.POST['birth_date']
            if not Person.objects.filter(national_code=post_request['national_code']):
                person.national_code = request.POST['national_code']
            person.save()
            person = Person.objects.get(national_code=post_request['national_code'])
            phones_box = Phone.objects.filter(Person_id=person.id)
            request_phone_list = request.POST.getlist('phone')
            # fixme: must be refactor
            for tel in range(len(request_phone_list)):
                if len(phones_box) > tel:
                    if not str(phones_box[tel]) == request_phone_list[tel]:
                        print(phones_box[tel], "==", request_phone_list[tel])
                        phones_box[tel].phone_number = request_phone_list[tel]
                        phones_box[tel].save()
            return self.get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['phones_box'] = Phone.objects.filter(Person_id=kwargs.get('object').id)
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
                            print(phone)
                            if not Phone.objects.filter(phone_number=phone):
                                Phone.objects.get_or_create(phone_number=phone, Person=person)
            context = {'form_person': form_person, 'form_phone': form_phone, 'phones_box': phones_box}
            return render(request, self.template_name, context)

    def get(self, request, **kwargs):
        form_person = PersonForm()
        form_phone = PhoneForm()
        context = {'form_person': form_person, 'form_phone': form_phone}
        return render(request, self.template_name, context)