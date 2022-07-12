from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import PersonSerializer, PatientStatusSerializer, StateSerializer
from hospital.models import Person, Phone, PatientStatus ,State
from .permissions import IsOwnerOrReadOnly
from .Filter import PersonFilter, PatientStatusFilter


class StandardSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000


class PersonListModelViewSet(viewsets.ModelViewSet):
    """
    Show list person and phones and Create Person and phone
    """
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    lookup_field = "national_code"
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PersonFilter
    search_fields = ['name', 'family', 'national_code']
    ordering_fields = ['created_date']
    pagination_class = StandardSetPagination

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        """Because our model Phone is of the type models.SET_NULL in remove custom """
        for phone in Phone.objects.filter(Person=instance.id):
            phone.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PatientStatusListModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = PatientStatusSerializer
    queryset = PatientStatus.objects.all()
    lookup_field = 'pk'
    ordering_fields = ['created_date']
    pagination_class = StandardSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PatientStatusFilter


class RegionListModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = StateSerializer
    queryset = State.objects.all()
    lookup_field = 'pk'