from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='question-circle')

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    health_interest = models.CharField(max_length=200, blank=True)
    expertise = models.CharField(max_length=200, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Question(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    upvotes = models.ManyToManyField(User, related_name='question_upvotes', blank=True)

    def total_upvotes(self):
        return self.upvotes.count()

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    upvotes = models.ManyToManyField(User, related_name='answer_upvotes', blank=True)
    is_expert = models.BooleanField(default=False)

    def total_upvotes(self):
        return self.upvotes.count()

    def __str__(self):
        return f"Answer to {self.question.title}"


class Journey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journeys')
    title = models.CharField(max_length=200)
    symptom = models.TextField()
    test = models.TextField(blank=True)
    doctor = models.CharField(max_length=200, blank=True)
    treatment = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username}'s journey: {self.title}"


# class ContactSubmission(models.Model):
#     name = models.CharField(max_length=100)
#     surname = models.CharField(max_length=100)
#     email = models.EmailField()
#     message = models.TextField()
#     is_not_robot = models.BooleanField(default=False)
#     submitted_at = models.DateTimeField(auto_now_add=True)
#     ip_address = models.GenericIPAddressField(null=True, blank=True)
#     user_agent = models.TextField(null=True, blank=True)
#
#     class Meta:
#         ordering = ['-submitted_at']
#
#     def __str__(self):
#         return f"{self.name} {self.surname} - {self.submitted_at.strftime('%Y-%m-%d')}"