
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class DonationPost(models.Model):
    title = models.CharField(max_length=200)
    child_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    medical_condition = models.TextField()

    report = models.ImageField(upload_to="medical_reports/")
    image = models.ImageField(upload_to="donation_images/", blank=True, null=True)

    target_amount = models.PositiveIntegerField()  # in INR
    raised_amount = models.PositiveIntegerField(default=0)

    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()

    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="donation_posts"
    )

    def remaining_amount(self):
        return max(self.target_amount - self.raised_amount, 0)

    def progress_percentage(self):
        return int((self.raised_amount / self.target_amount) * 100)

    def __str__(self):
        return self.title


class Donation(models.Model):
    post = models.ForeignKey(DonationPost, on_delete=models.CASCADE, related_name="donations")
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)

    amount = models.PositiveIntegerField()  # INR
    razorpay_payment_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} → {self.post.title}"


