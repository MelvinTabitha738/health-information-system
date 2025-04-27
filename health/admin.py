# health/admin.py

from django.contrib import admin
from .models import HealthProgram, Client, Enrollment

@admin.register(HealthProgram)
class HealthProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'gender', 'date_of_birth', 'contact_number', 'registration_date')
    list_filter = ('gender', 'registration_date')
    search_fields = ('first_name', 'last_name', 'contact_number', 'email')
    date_hierarchy = 'registration_date'
    
    readonly_fields = ('age',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'age', 'gender')
        }),
        ('Contact Details', {
            'fields': ('contact_number', 'email', 'address')
        }),
        ('Registration', {
            'fields': ('registration_date',)
        }),
    )

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'program', 'enrollment_date')
    list_filter = ('program', 'enrollment_date')
    search_fields = ('client__first_name', 'client__last_name', 'program__name')
    date_hierarchy = 'enrollment_date'
    
    autocomplete_fields = ['client', 'program']