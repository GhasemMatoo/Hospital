from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import PersonSerializer
from hospital.models import Person, Phone
from .permissions import IsOwnerOrReadOnly


class PersonListModelViewSet(viewsets.ModelViewSet):
    """
    Show list person and phones and Create Person and phone
    """
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    lookup_field = "national_code"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        """Because our model Phone is of the type models.SET_NULL in remove custom """
        for phone in Phone.objects.filter(Person=instance.id):
            phone.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)