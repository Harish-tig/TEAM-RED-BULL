from django.contrib import admin
from .models import (
    Category,
    UserProfile,
    Question,
    Answer,
    Journey
)


# ================= CATEGORY =================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "icon")
    search_fields = ("name",)
    ordering = ("name",)


# ================= USER PROFILE =================
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "health_interest", "expertise")
    search_fields = ("user__username", "health_interest", "expertise")


# ================= ANSWER INLINE =================
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    fields = ("user", "text", "is_expert", "created_at")
    readonly_fields = ("created_at",)


# ================= QUESTION =================
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "category",
        "created_at",
        "total_upvotes",
    )
    list_filter = ("category", "created_at")
    search_fields = ("title", "description", "user__username")
    date_hierarchy = "created_at"
    inlines = [AnswerInline]

    def total_upvotes(self, obj):
        return obj.upvotes.count()
    total_upvotes.short_description = "Upvotes"


# ================= ANSWER =================
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        "question",
        "user",
        "is_expert",
        "created_at",
        "total_upvotes",
    )
    list_filter = ("is_expert", "created_at")
    search_fields = ("text", "user__username", "question__title")

    def total_upvotes(self, obj):
        return obj.upvotes.count()
    total_upvotes.short_description = "Upvotes"


# ================= JOURNEY =================
@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "doctor",
        "date",
        "created_at",
    )
    list_filter = ("date", "created_at")
    search_fields = (
        "title",
        "symptom",
        "doctor",
        "user__username",
    )
    date_hierarchy = "date"