from django.contrib import admin
from .models import ContactSubmission

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'email', 'submitted_at')
    list_filter = ('submitted_at', 'is_not_robot')
    search_fields = ('name', 'surname', 'email', 'message')
    readonly_fields = ('submitted_at', 'ip_address', 'user_agent')