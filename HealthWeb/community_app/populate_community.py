from community_app.models import Category, User, UserProfile


# Create categories
categories = [
    ('General Health', 'fas fa-heartbeat'),
    ('Cardiology', 'fas fa-heart'),
    ('Neurology', 'fas fa-brain'),
    ('Dermatology', 'fas fa-allergies'),
    ('Mental Health', 'fas fa-brain'),
    ('Pediatrics', 'fas fa-baby'),
    ('Orthopedics', 'fas fa-bone'),
    ('Gastroenterology', 'fas fa-stomach'),
    ('Urology', 'fas fa-tint'),
    ('Gynecology', 'fas fa-female'),
]

for name, icon in categories:
    Category.objects.get_or_create(name=name, icon=icon)

print("Sample categories created!")