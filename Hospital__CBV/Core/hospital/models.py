from django.db import models

# Create your models here.


class MainModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Person(MainModel):

    name = models.CharField(max_length=50, null=True)
    family = models.CharField(max_length=50, null=True)
    national_code = models.CharField(max_length=11, unique=True)
    id_number = models.CharField(max_length=30, null=True, blank=True)
    birth_date = models.DateField()
    region = models.ForeignKey('City', on_delete=models.CASCADE, null=True, blank=True, related_name='cities')

    def __str__(self):
        return f"{self.name} {self.family}"


class Phone(MainModel):

    phone_number = models.CharField(max_length=11, unique=True)
    Person = models.ForeignKey('Person', on_delete=models.SET_NULL, blank=True, null=True, related_name='Person')

    def __str__(self):
        return self.phone_number


class PatientStatus(MainModel):
    doctor_name = models.CharField(max_length=100, null=True)
    type_disease = models.TextField(null=True)
    invoice = models.IntegerField(default=0)
    franchise = models.IntegerField(default=0)
    hosp_time = models.DateTimeField(auto_now=True)
    clearance_time = models.DateTimeField(null=True)
    Person = models.ForeignKey('Person', on_delete=models.CASCADE,
                               blank=True, null=True, related_name='Person_PatientStatus')

    def __str__(self):
        return self.type_disease


class State(MainModel):

    state = models.CharField(max_length=50)

    def __str__(self):
        return self.state


class City(MainModel):

    city = models.CharField(max_length=50)
    state = models.ForeignKey('State', on_delete=models.CASCADE, related_name='stat_city')

    def __str__(self):
        return self.city
