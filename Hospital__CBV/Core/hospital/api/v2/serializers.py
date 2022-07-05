from rest_framework import serializers
from hospital.models import Person, Phone, PatientStatus


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ['id', 'phone_number']


class PersonSerializer(serializers.ModelSerializer):
    phones = PhoneSerializer(source='Person', many=True, read_only=True)
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ['id', 'absolute_url', 'name', 'family', 'national_code', 'id_number', 'birth_date', 'phones']

    def get_absolute_url(self, obj):
        # Create urls py object
       URL = self.context.get('request').build_absolute_uri(obj.national_code)
       return URL

    def to_representation(self, instance):
        # Cut in absolute_url to Show on object
        request = self.context.get('request')
        representation = super().to_representation(instance)
        if request.parser_context.get('kwargs'):
            representation.pop('absolute_url')
        return representation

    def create(self, validated_data):
        person_instance = Person.objects.create(**validated_data)
        for phone in self.initial_data["phones"]:
            if not Phone.objects.filter(phone_number=phone["phone_number"]):
                Phone.objects.get_or_create(phone_number=phone["phone_number"], Person=person_instance)
        return person_instance

    def update(self, instance, validated_data):
        for phone in self.initial_data["phones"]:
            phone_object = Phone.objects.get(id=phone["id"])
            if not Phone.objects.filter(phone_number=phone["phone_number"]):
                phone_object.phone_number = phone["phone_number"]
                phone_object.save()
        return super(PersonSerializer, self).update(instance, validated_data)


class PatientStatusSerializer(serializers.ModelSerializer):
    Persons = PersonSerializer(source='Person')
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = PatientStatus
        fields = ['id', 'absolute_url', 'doctor_name', 'invoice', 'franchise',
                  'hosp_time', 'clearance_time', 'type_disease', 'Persons']

    def get_absolute_url(self, obj):
        # Create urls py object
       URL = self.context.get('request').build_absolute_uri(obj.id)
       return URL

    def to_representation(self, instance):
        # Cut in absolute_url to Show on object
        request = self.context.get('request')
        representation = super().to_representation(instance)
        if request.parser_context.get('kwargs'):
            representation.pop('absolute_url')
        return representation
