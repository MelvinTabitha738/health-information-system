# health/tests.py

from django.test import TestCase, Client as TestClient
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status

from .models import HealthProgram, Client, Enrollment
from datetime import date

class HealthProgramModelTests(TestCase):
    """Test cases for HealthProgram model"""
    
    def test_health_program_creation(self):
        """Test creating a health program"""
        program = HealthProgram.objects.create(
            name="Tuberculosis Treatment",
            description="Program for TB treatment and monitoring"
        )
        self.assertEqual(program.name, "Tuberculosis Treatment")
        self.assertTrue(program.created_at is not None)
        self.assertTrue(program.updated_at is not None)

class ClientModelTests(TestCase):
    """Test cases for Client model"""
    
    def test_client_creation(self):
        """Test creating a client"""
        client = Client.objects.create(
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1990, 1, 1),
            gender="M",
            contact_number="1234567890",
            email="john@example.com",
            address="123 Main St"
        )
        self.assertEqual(client.full_name, "John Doe")
        self.assertTrue(isinstance(client.age, int))
        self.assertEqual(client.gender, "M")

class EnrollmentModelTests(TestCase):
    """Test cases for Enrollment model"""
    
    def setUp(self):
        """Set up test data"""
        self.program = HealthProgram.objects.create(
            name="HIV Support",
            description="Program for HIV/AIDS support and treatment"
        )
        self.client = Client.objects.create(
            first_name="Jane",
            last_name="Smith",
            date_of_birth=date(1985, 5, 15),
            gender="F",
            contact_number="9876543210",
            email="jane@example.com",
            address="456 Oak St"
        )
    
    def test_enrollment_creation(self):
        """Test enrolling a client in a program"""
        enrollment = Enrollment.objects.create(
            client=self.client,
            program=self.program,
            notes="Initial enrollment"
        )
        self.assertEqual(enrollment.client, self.client)
        self.assertEqual(enrollment.program, self.program)
        self.assertTrue(enrollment.enrollment_date is not None)

class ViewTests(TestCase):
    """Test cases for views"""
    
    def setUp(self):
        """Set up test data and test client"""
        self.client = TestClient()
        self.program = HealthProgram.objects.create(
            name="Malaria Prevention",
            description="Program for malaria prevention and treatment"
        )
        self.test_client = Client.objects.create(
            first_name="Test",
            last_name="User",
            date_of_birth=date(1995, 10, 10),
            gender="M",
            contact_number="5555555555",
            email="test@example.com",
            address="789 Pine St"
        )
    
    def test_dashboard_view(self):
        """Test the dashboard view"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'health/dashboard.html')
    
    def test_client_list_view(self):
        """Test the client list view"""
        response = self.client.get(reverse('client_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'health/client_list.html')
        self.assertContains(response, "Test User")
    
    def test_client_detail_view(self):
        """Test the client detail view"""
        response = self.client.get(reverse('client_detail', kwargs={'pk': self.test_client.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'health/client_detail.html')
        self.assertContains(response, "Test User")
    
    def test_program_list_view(self):
        """Test the program list view"""
        response = self.client.get(reverse('program_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'health/program_list.html')
        self.assertContains(response, "Malaria Prevention")

class APITests(APITestCase):
    """Test cases for API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.program = HealthProgram.objects.create(
            name="Diabetes Management",
            description="Program for diabetes management and support"
        )
        self.client_obj = Client.objects.create(
            first_name="API",
            last_name="Test",
            date_of_birth=date(1980, 3, 20),
            gender="F",
            contact_number="1112223333",
            email="api@example.com",
            address="101 API St"
        )
        Enrollment.objects.create(
            client=self.client_obj,
            program=self.program,
            notes="API test enrollment"
        )
    
    def test_client_list_api(self):
        """Test the client list API endpoint"""
        url = reverse('api-client-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'API')
    
    def test_client_detail_api(self):
        """Test the client detail API endpoint"""
        url = reverse('api-client-detail', kwargs={'pk': self.client_obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'api@example.com')
        self.assertEqual(len(response.data['enrollments']), 1)
        self.assertEqual(response.data['enrollments'][0]['program']['name'], 'Diabetes Management')
    
    def test_program_list_api(self):
        """Test the program list API endpoint"""
        url = reverse('api-program-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Diabetes Management')