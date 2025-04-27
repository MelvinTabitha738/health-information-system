# health/serializers.py

from rest_framework import serializers
from .models import Client, HealthProgram, Enrollment

class HealthProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthProgram
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']

class EnrollmentSerializer(serializers.ModelSerializer):
    program_name = serializers.ReadOnlyField(source='program.name')
    
    class Meta:
        model = Enrollment
        fields = ['id', 'client', 'program', 'program_name', 'enrollment_date', 'notes']

class ClientSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField()
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'full_name', 'date_of_birth', 
                 'age', 'gender', 'contact_number', 'email', 'address', 
                 'registration_date']

class ClientDetailSerializer(ClientSerializer):
    """
    Detailed client serializer that includes program enrollments
    """
    enrollments = serializers.SerializerMethodField()
    
    class Meta(ClientSerializer.Meta):
        fields = ClientSerializer.Meta.fields + ['enrollments']
    
    def get_enrollments(self, obj):
        enrollments = Enrollment.objects.filter(client=obj)
        return [
            {
                'id': enrollment.id,
                'program': {
                    'id': enrollment.program.id,
                    'name': enrollment.program.name,
                    'description': enrollment.program.description
                },
                'enrollment_date': enrollment.enrollment_date,
                'notes': enrollment.notes
            }
            for enrollment in enrollments
        ]