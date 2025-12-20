from django.contrib import admin

from django.contrib import admin
from .models import DonationPost, Donation

@admin.register(DonationPost)
class DonationPostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "child_name",
        "target_amount",
        "raised_amount",
        "is_active",
        "end_date",
    )
    readonly_fields = ("raised_amount",)
    search_fields = ("title", "child_name")
    list_filter = ("is_active",)

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("post", "amount", "razorpay_payment_id", "created_at")

