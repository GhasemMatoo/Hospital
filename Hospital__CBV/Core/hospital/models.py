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
    region = models.ForeignKey('State', on_delete=models.CASCADE, null=True, blank=True)
    file_patient = models.ForeignKey('PatientStatus', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.family}"


class Phone(MainModel):

    phone_number = models.CharField(max_length=11,unique=True)
    Person = models.ForeignKey('Person', on_delete=models.SET_NULL,blank=True, null=True)

    def __str__(self):
        return self.phone_number


class PatientStatus(MainModel):
    type_disease = models.CharField(max_length=100, null=True)
    invoice = models.IntegerField(default=0)
    franchise = models.IntegerField(default=0)
    hosp_time = models.DateTimeField(auto_now=True)
    clearance_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.type_disease


class State(MainModel):

    state = models.CharField(max_length=20)

    def __str__(self):
        return self.state


class City(MainModel):

    city = models.CharField(max_length=20)
    state = models.ForeignKey('State', on_delete=models.CASCADE)

    def __str__(self):
        return self.city
