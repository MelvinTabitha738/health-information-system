"""
URL configuration for health_info_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# health_info_system/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from health import views
from health import api

# API Router
router = DefaultRouter()
router.register(r'clients', api.ClientViewSet, basename='api-client')
router.register(r'programs', api.HealthProgramViewSet, basename='api-program')
router.register(r'enrollments', api.EnrollmentViewSet, basename='api-enrollment')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Health Program URLs
    path('programs/', views.HealthProgramListView.as_view(), name='program_list'),
    path('programs/add/', views.HealthProgramCreateView.as_view(), name='program_create'),
    path('programs/<int:pk>/edit/', views.HealthProgramUpdateView.as_view(), name='program_update'),
    path('programs/<int:pk>/delete/', views.HealthProgramDeleteView.as_view(), name='program_delete'),
    
    # Client URLs
    path('clients/', views.ClientListView.as_view(), name='client_list'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('clients/add/', views.ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/edit/', views.ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),
    
    # Enrollment URLs
    path('clients/<int:client_id>/enroll/', views.enroll_client, name='enroll_client'),
    path('enrollments/<int:enrollment_id>/unenroll/', views.unenroll_client, name='unenroll_client'),
    
    # API URLs
    path('api/', api.api_root, name='api-root'),
    path('api/', include(router.urls)),
]
