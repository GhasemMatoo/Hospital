from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PersonSerializer
from hospital.models import Person, Phone
from django.shortcuts import get_list_or_404


@api_view(['GET', 'POST'])
def person_views(request):
    person = Person.objects.all()
    if request.method == 'GET':
        serializer = PersonSerializer(data=person, many=True)
        serializer.is_valid()
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PersonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def person_detail_views(request, national_code):
    person = get_list_or_404(Person, national_code=national_code)
    if request.method == 'GET':
        serializer = PersonSerializer(data=person, many=True)
        serializer.is_valid()
        return Response(serializer.data)
    elif request.method == 'PUT':
        person = Person.objects.get(national_code=national_code)
        serializer = PersonSerializer(person, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        person = Person.objects.get(national_code=national_code)
        for phone in Phone.objects.filter(Person=person.id):
            phone.delete()
        person.delete()
        return Response({"detail": "Item removed successfully"}, status=status.HTTP_204_NO_CONTENT)