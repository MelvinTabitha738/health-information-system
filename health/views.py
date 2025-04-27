# health/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import HealthProgram, Client, Enrollment
from .forms import HealthProgramForm, ClientForm, EnrollmentForm, ClientSearchForm

# Health Program Views
class HealthProgramListView(ListView):
    model = HealthProgram
    template_name = 'health/program_list.html'
    context_object_name = 'programs'

class HealthProgramCreateView(CreateView):
    model = HealthProgram
    form_class = HealthProgramForm
    template_name = 'health/program_form.html'
    success_url = reverse_lazy('program_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Health program created successfully!')
        return super().form_valid(form)

class HealthProgramUpdateView(UpdateView):
    model = HealthProgram
    form_class = HealthProgramForm
    template_name = 'health/program_form.html'
    success_url = reverse_lazy('program_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Health program updated successfully!')
        return super().form_valid(form)

class HealthProgramDeleteView(DeleteView):
    model = HealthProgram
    template_name = 'health/program_confirm_delete.html'
    success_url = reverse_lazy('program_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Health program deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Client Views
class ClientListView(ListView):
    model = Client
    template_name = 'health/client_list.html'
    context_object_name = 'clients'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        form = ClientSearchForm(self.request.GET)
        if form.is_valid():
            search_query = form.cleaned_data.get('search_query')
            if search_query:
                queryset = queryset.filter(
                    Q(first_name__icontains=search_query) | 
                    Q(last_name__icontains=search_query) | 
                    Q(contact_number__icontains=search_query)
                )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ClientSearchForm(self.request.GET)
        return context

class ClientDetailView(DetailView):
    model = Client
    template_name = 'health/client_detail.html'
    context_object_name = 'client'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.get_object()
        context['enrollments'] = Enrollment.objects.filter(client=client)
        context['enrollment_form'] = EnrollmentForm(client=client)
        return context

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'health/client_form.html'
    success_url = reverse_lazy('client_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Client registered successfully!')
        return super().form_valid(form)

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'health/client_form.html'
    
    def get_success_url(self):
        return reverse_lazy('client_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Client information updated successfully!')
        return super().form_valid(form)

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'health/client_confirm_delete.html'
    success_url = reverse_lazy('client_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Client deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Enrollment Views
def enroll_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    
    if request.method == 'POST':
        form = EnrollmentForm(request.POST, client=client)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.client = client
            enrollment.save()
            messages.success(request, f'Client enrolled in {enrollment.program.name} program successfully!')
            return redirect('client_detail', pk=client_id)
    else:
        form = EnrollmentForm(client=client)
    
    return render(request, 'health/enrollment_form.html', {
        'form': form,
        'client': client
    })

def unenroll_client(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, pk=enrollment_id)
    client_id = enrollment.client.id
    program_name = enrollment.program.name
    
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, f'Client unenrolled from {program_name} program successfully!')
        return redirect('client_detail', pk=client_id)
    
    return render(request, 'health/unenroll_confirm.html', {
        'enrollment': enrollment
    })

# Dashboard View
def dashboard(request):
    # Basic statistics for the dashboard
    total_clients = Client.objects.count()
    total_programs = HealthProgram.objects.count()
    total_enrollments = Enrollment.objects.count()
    
    recent_clients = Client.objects.order_by('-registration_date')[:5]
    recent_enrollments = Enrollment.objects.order_by('-enrollment_date')[:5]
    
    context = {
        'total_clients': total_clients,
        'total_programs': total_programs,
        'total_enrollments': total_enrollments,
        'recent_clients': recent_clients,
        'recent_enrollments': recent_enrollments,
    }
    
    return render(request, 'health/dashboard.html', context)