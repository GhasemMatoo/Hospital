from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .serializers import PersonSerializer
from hospital.models import Person, Phone


class PersonList(ListCreateAPIView):
    """
    Show list person and phones and Create Person and phone
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PersonSerializer
    queryset = Person.objects.all()


class PersonDetail(RetrieveUpdateDestroyAPIView):
    """
    Show Person and phones in Update and Delete
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    lookup_field = "national_code"

    def delete(self, request, national_code):
        """Because our model Phone is of the type models.SET_NULL in remove custom """
        person = Person.objects.get(national_code=national_code)
        for phone in Phone.objects.filter(Person=person.id):
            phone.delete()
        person.delete()
        return Response({"detail": "Item removed successfully"}, status=status.HTTP_204_NO_CONTENT)
