from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from .models import ContactSubmission
from community_app.views import login_view, home as h2, register
import random
from datetime import datetime, timedelta

def home(request):
    return render(request, 'home/index.html')


def articles(request):
    return render(request, 'articles/index.html')


def about(request):
    return render(request, 'about/index.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get user info for logging
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            user_agent = request.META.get('HTTP_USER_AGENT', '')

            # Save form with additional info
            contact = form.save(commit=False)
            contact.ip_address = ip
            contact.user_agent = user_agent
            contact.save()

            messages.success(request, 'Thank you for contacting us! We will get back to you within 24 business hours.')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contactus/contactus.html', {'form': form})


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def terms_and_conditions(request):
    return render(request, 'terms.html')


def sitemap(request):
    return render(request, 'sitemap.html')


def redirect_login(request):
    if request.user.is_authenticated:
        return h2(request)
    return login_view(request=request)

def redirect_register(request):
    return register(request=request)

def find_doctor(request):
    # Generate fake doctor data
    specialities = [
        'General Practitioner', 'Cardiologist', 'Dermatologist',
        'Pediatrician', 'Orthopedic Surgeon', 'Neurologist',
        'Gynecologist', 'Psychiatrist', 'Dentist', 'Ophthalmologist',
        'ENT Specialist', 'Urologist', 'Endocrinologist', 'Oncologist'
    ]

    locations = [
        'Cape Town', 'Johannesburg', 'Durban', 'Pretoria',
        'Port Elizabeth', 'Bloemfontein', 'East London', 'Nelspruit'
    ]

    # Generate 15 fake doctors
    doctors = []
    for i in range(15):
        doctor = {
            'id': i + 1,
            'name': f'Dr. {["James", "Sarah", "Michael", "Lisa", "David", "Emma", "Robert", "Grace"][i % 8]} {["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"][i % 8]}',
            'speciality': random.choice(specialities),
            'location': random.choice(locations),
            'experience': f'{random.randint(1, 35)} years',
            'charges': f'R{random.randint(500, 2500)}',
            'rating': round(random.uniform(3.5, 5.0), 1),
            'status': random.choice(['Available', 'Available', 'Available', 'Busy']),  # 75% available
            'phone': f'+27 {random.randint(11, 99)} {random.randint(100, 999)} {random.randint(1000, 9999)}',
            'next_available': (
                        datetime.now() + timedelta(days=random.randint(0, 3), hours=random.randint(1, 8))).strftime(
                '%Y-%m-%d %H:%M'),
            'image_url': f'https://i.pravatar.cc/150?img={i + 1}',  # Placeholder images
        }
        doctors.append(doctor)

    context = {
        'specialities': sorted(specialities),
        'locations': sorted(locations),
        'doctors': doctors,
        'map_api_key': 'YOUR_GOOGLE_MAPS_API_KEY',  # Replace with actual key
        'default_location': '-33.9249,18.4241',  # Cape Town coordinates
        'default_zoom': 10,
    }

    return render(request, 'find_doctor/index.html', context)