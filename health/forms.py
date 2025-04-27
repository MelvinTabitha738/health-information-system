# health/forms.py

from django import forms
from .models import Client, HealthProgram, Enrollment

class HealthProgramForm(forms.ModelForm):
    """
    Form for creating and updating health programs
    """
    class Meta:
        model = HealthProgram
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ClientForm(forms.ModelForm):
    """
    Form for registering and updating clients
    """
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'date_of_birth', 
                  'gender', 'contact_number', 'email', 'address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class EnrollmentForm(forms.ModelForm):
    """
    Form for enrolling clients in health programs
    """
    class Meta:
        model = Enrollment
        fields = ['program', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        client = kwargs.pop('client', None)
        super(EnrollmentForm, self).__init__(*args, **kwargs)
        
        if client:
            # Exclude programs that the client is already enrolled in
            enrolled_programs = client.programs.all()
            self.fields['program'].queryset = HealthProgram.objects.exclude(
                id__in=[program.id for program in enrolled_programs]
            )

class ClientSearchForm(forms.Form):
    """
    Form for searching clients
    """
    search_query = forms.CharField(
        max_length=100, 
        required=False, 
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by name or contact number',
            'class': 'form-control'
        })
    )