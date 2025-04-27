# health/api.py

from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Client, HealthProgram, Enrollment
from .serializers import ClientSerializer, HealthProgramSerializer, EnrollmentSerializer, ClientDetailSerializer

@api_view(['GET'])
def api_root(request, format=None):
    """
    API root endpoint showing available endpoints
    """
    return Response({
        'clients': reverse('api-client-list', request=request, format=format),
        'programs': reverse('api-program-list', request=request, format=format),
        'enrollments': reverse('api-enrollment-list', request=request, format=format),
    })

class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint for clients
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'contact_number']
    
    def get_serializer_class(self):
        # Use detailed serializer for retrieve action
        if self.action == 'retrieve':
            return ClientDetailSerializer
        return ClientSerializer

class HealthProgramViewSet(viewsets.ModelViewSet):
    """
    API endpoint for health programs
    """
    queryset = HealthProgram.objects.all()
    serializer_class = HealthProgramSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for enrollments
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer