from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .serializers import PersonSerializer
from hospital.models import Person, Phone
from django.shortcuts import get_list_or_404

class PersonList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PersonSerializer

    def get(self, request):
        """
        Return a list of all person and phones
        """
        person = Person.objects.all()
        serializer = PersonSerializer(data=person, many=True)
        serializer.is_valid()
        return Response(serializer.data)

    def post(self, request):
        """
        Create person and phones
        """
        serializer = PersonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PersonDetail(APIView):
    """
    Show Person and phones in Update and Delete
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PersonSerializer

    def get(self, request, national_code):
        """Show in Person and phones"""
        person = get_list_or_404(Person, national_code=national_code)
        serializer = PersonSerializer(data=person, many=True)
        serializer.is_valid()
        return Response(serializer.data)

    def put(self, request, national_code):
        """Update in person and phones"""
        person = Person.objects.get(national_code=national_code)
        serializer = PersonSerializer(person, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, national_code):
        person = Person.objects.get(national_code=national_code)
        for phone in Phone.objects.filter(Person=person.id):
            phone.delete()
        person.delete()
        return Response({"detail": "Item removed successfully"}, status=status.HTTP_204_NO_CONTENT)
