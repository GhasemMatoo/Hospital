from django.contrib import admin
from hospital.models import Person, PatientStatus, Phone, City, State


# Register your models here.


class PersonAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    list_display = ('__str__', 'national_code', 'update_date')
    list_filter = ['national_code']
    search_fields = ['national_code', 'name', 'family']


class PhoneAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    list_display = ('phone_number', 'person_first_name')
    list_filter = ['phone_number']
    search_fields = ['phone_number ']

    @admin.display()
    def person_first_name(self, obj):
        return f"{obj.Person.name} {obj.Person.family}==>{obj.Person.national_code}"


admin.site.register(Person, PersonAdmin)
admin.site.register(PatientStatus)
admin.site.register(Phone, PhoneAdmin)
admin.site.register(City)
admin.site.register(State)
