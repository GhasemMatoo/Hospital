from django.contrib import admin
from .models import Person, PatientStatus, Phone, City, State
# Register your models here.


class PersonAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    list_display = ('__str__', 'national_code', 'update_date')
    # list_filter = ['national_code']
    # search_fields = ['national_code', 'name', 'family']


class PatientStatusAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    list_display = ('__str__', 'doctor_name', 'hosp_time', 'clearance_time')
    # list_filter = ['type_disease', 'doctor_name']
    # search_fields = ['type_disease', 'doctor_name']


class PhoneAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    list_display = ('phone_number', 'person_first_name')
    # list_filter = ['phone_number']
    # search_fields = ['phone_number ']

    '''
    set admin display in field person_first_name
    '''
    @admin.display()
    def person_first_name(self, obj):
        return f"{obj.Person.name} {obj.Person.family}==>{obj.Person.national_code}"


admin.site.register(Person, PersonAdmin)
admin.site.register(PatientStatus, PatientStatusAdmin)
admin.site.register(Phone, PhoneAdmin)
admin.site.register(City)
admin.site.register(State)
