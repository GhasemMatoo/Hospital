from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .serializers import PersonSerializer
from hospital.models import Person, Phone
from django.shortcuts import get_list_or_404


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def person_views(request):
    """
    Show persons in list phones
    """
    person = Person.objects.all()
    if request.method == 'GET':
        serializer = PersonSerializer(data=person, many=True)
        serializer.is_valid()
        return Response(serializer.data)
    elif request.method == 'POST':
        """
        Crate person and phones
        """
        serializer = PersonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def person_detail_views(request, national_code):
    if request.method == 'GET':
        """
          Show person in list phones
        """
        person = get_list_or_404(Person, national_code=national_code)
        serializer = PersonSerializer(data=person, many=True)
        serializer.is_valid()
        return Response(serializer.data)
    elif request.method == 'PUT':
        """
        Update person and phones
        """
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