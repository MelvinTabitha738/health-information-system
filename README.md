# Health Information System Project
# Health Information System

A Django-based application for managing health programs and client enrollments. This system allows health professionals to manage client information, create health programs, and enroll clients in these programs.

**▶️ [Watch Project Demo] (https://drive.google.com/file/d/1svz1HYFXggb3EBjVV-pEwl15sFYrHW9o/view?usp=drive_link)

view my powerpoint presentation here https://docs.google.com/presentation/d/1UJRAv0umRdQJZZs2_yJKEqpb2k0Ojoqp/edit?usp=drive_link&ouid=103422223415698607917&rtpof=true&sd=true

## Features

- **Dashboard** with summary statistics and recent activity
- **Health Program Management**
  - Create, edit, and delete health programs (e.g., TB, Malaria, HIV)
  - View list of all programs
- **Client Management**
  - Register new clients with personal and contact information
  - Search for clients by name or contact number
  - View client profiles with detailed information
  - Update client information
- **Program Enrollment**
  - Enroll clients in one or more health programs
  - Unenroll clients from programs
  - View enrollments for each client
- **API Access**
  - REST API for accessing client profiles and program information
  - API endpoints for integration with other systems

## Technology Stack

- **Backend**: Django 4.2+ with Python 3.8+
- **Frontend**: Bootstrap 5 for responsive design
- **API**: Django REST Framework
- **Database**: SQLite (development), can be configured for PostgreSQL in production
- **Testing**: Django Test Framework with coverage

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/health_information_system.git
   cd health_information_system
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

## Project Structure

```
health_information_system/
│
├── health_info_system/     # Django project settings
│   ├── settings.py         # Project settings
│   ├── urls.py             # Main URL routing
│   └── wsgi.py             # WSGI configuration
│
├── health/                 # Main app directory
│   ├── models.py           # Database models
│   ├── views.py            # View functions and classes
│   ├── forms.py            # Form definitions
│   ├── api.py              # API views and endpoints
│   ├── serializers.py      # DRF serializers
│   ├── admin.py            # Admin site configuration
│   ├── tests.py            # Unit tests
│   └── urls.py             # App-specific URLs
│
├── templates/              # HTML templates
│   ├── base.html           # Base template with layout
│   └── health/             # App-specific templates
│
├── static/                 # Static files (CSS, JS, images)
│
├── manage.py               # Django management script
└── requirements.txt        # Project dependencies
```

## API Endpoints

- `/api/` - API root with links to all endpoints
- `/api/clients/` - List all clients (GET) or create a new client (POST)
- `/api/clients/{id}/` - Get client details including enrollments
- `/api/programs/` - List all health programs
- `/api/programs/{id}/` - Get program details
- `/api/enrollments/` - List all enrollments or create new enrollments

## Security Considerations

- User authentication is handled through Django's built-in authentication system
- Client data is protected through proper access controls
- Form validation ensures data integrity
- API endpoints can be secured with token authentication for production use

## Testing

Run tests with:
```bash
python manage.py test
```

For coverage report:
```bash
coverage run --source='.' manage.py test
coverage report
```

## Future Enhancements

- User role-based permissions
- Client medical history tracking
- Appointment scheduling
- Reporting and analytics
- Mobile application integration

## License

This project is licensed under the MIT License.
