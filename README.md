# Doctor Appointment Booking System

A Django REST API-based system for managing doctor appointments. This system allows patients to book appointments with doctors while maintaining scheduling constraints and providing comprehensive management features for both doctors and patients.

# Front end is in progress

## Features

### For Doctors
- Create and manage professional profile
- View and manage appointments
- Accept/reject appointment requests
- Automatic time slot management (10 AM - 5 PM)
- Lunch break handling (1 PM - 2 PM)
- 30-minute appointment slots

### For Patients
- Create and manage personal profile
- Book appointments with doctors
- View appointment history
- Cancel existing appointments
- Multiple doctor booking support

### System Features
- JWT Authentication
- Role-based access control
- Double booking prevention
- Automated time slot management
- Appointment status tracking

## Technical Requirements

- Python 3.8+
- Django 3.2+
- Django REST Framework
- djangorestframework-simplejwt

## Installation

1. Clone the repository
```bash
git clone https://github.com/nelsonct7/doctors-slot-booking-upgraded
cd doctor-appointment-system
```
2. Create and activate virtual environment using anaconda
```bash
url https://docs.anaconda.com/working-with-conda/environments/
conda env create -f condaEnv.yaml
```
3. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```
4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
5. Create superuser
```bash
python manage.py createsuperuser
```
6. Run the development server
```bash
python manage.py runserve
```

# API Endpoints
## Authentication
POST /api/signup/ - Register new user (doctor/patient)

POST /api/login/ - Obtain JWT token

## Doctors
GET /api/doctors/ - List all doctors

GET /api/doctors/{id}/ - Get doctor details

PUT /api/doctors/{id}/ - Update doctor profile

DELETE /api/doctors/{id}/ - Delete doctor profile

GET /api/doctors/{id}/available_slots/ - Get available time slots

POST /api/doctors/{id}/accept_appointment/ - Accept appointment

POST /api/doctors/{id}/reject_appointment/ - Reject appointment

## Patients
GET /api/patients/{id}/ - Get patient profile

PUT /api/patients/{id}/ - Update patient profile

DELETE /api/patients/{id}/ - Delete patient profile

POST /api/patients/{id}/book_appointment/ - Book appointment

POST /api/patients/{id}/cancel_appointment/ - Cancel appointment

GET /api/patients/{id}/my_appointments/ - List patient's appointments

# Data Models

## Doctor
```bash
- user (OneToOne with Django User)
- specialization
- license_number
- is_verified
- phone_number
- address
```

## Patient
```bash
- user (OneToOne with Django User)
- date_of_birth
- blood_group
- phone_number
- address
- emergency_contact
- is_verified
```

## Appointment
```bash
- doctor (ForeignKey)
- patient (ForeignKey)
- date
- time_slot
- status (pending/accepted/rejected/cancelled)
```

# Business Rules
1. Appointment Booking
    One patient cannot book multiple appointments in the same time slot

    One patient cannot book appointments with multiple doctors in the same time slot

    Patients can book different time slots with different doctors 

2. Time Slots
    Available from 10 AM to 5 PM

    Lunch break from 1 PM to 2 PM

    Each slot is 30 minutes

    No overlapping appointments

3. Verification
    Both doctors and patients must be verified to use the system

    Only authenticated users can access the API

# Security Features
    JWT Authentication

    Permission-based access control

    User verification system

    Protected API endpoints

    Secure password handling

# Error Handling
The API includes comprehensive error handling for:


    Invalid appointments

    Double booking attempts

    Time slot conflicts

    Authentication errors

    Resource not found

    Permission denied

# Contributing
    Fork the repository

    Create your feature branch

    Commit your changes

    Push to the branch

    Create a new Pull Request

# License

    This project is licensed under the MIT License.

```bash

This README provides a comprehensive overview of the system, including installation instructions, API endpoints, data models, and business rules. It serves as both documentation and a quick-start guide for developers who want to use or contribute to the project.

```

