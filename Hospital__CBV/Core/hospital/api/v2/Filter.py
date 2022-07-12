from django_filters import rest_framework as filters
from hospital.models import Person, PatientStatus


class PersonFilter(filters.FilterSet):
    """
    Filter for person fields medal and Date fields start date to end
    """
    created_date = filters.DateFromToRangeFilter()

    class Meta:
        model = Person
        fields = ['name', 'family', 'national_code', 'region__state', 'region', 'birth_date']


class PatientStatusFilter(filters.FilterSet):
    """
    Filter for person fields medal and Date fields start date to end
    """
    hosp_time = filters.DateFromToRangeFilter()

    class Meta:
        model = PatientStatus
        fields = ['doctor_name', 'invoice', 'hosp_time', 'Person__name', 'Person__family',
                  'Person__id_number', 'Person__national_code', 'Person__birth_date', 'Person__region__state',
                  'Person__region']