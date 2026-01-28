from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser, Payment


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Админка кастомного пользователя."""

    list_display = ("email", "phone", "city", "is_staff", "date_joined")
    list_filter = ("is_staff", "is_active", "date_joined")
    search_fields = ("email", "phone", "city")
    ordering = ("email",)  # ← Явно переопределяем ordering

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Личная информация", {"fields": ("phone", "city", "avatar")}),
        (
            "Права",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "phone",
                    "city",
                    "avatar",
                ),
            },
        ),
    )
    readonly_fields = ("last_login", "date_joined")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Админка платежей."""

    list_display = (
        "id",
        "user",
        "amount",
        "course",
        "lesson",
        "payment_date",
        "payment_method",
        "status",
    )
    list_filter = ("payment_method", "status", "course", "lesson")
    search_fields = ("user__email", "course__title")
    readonly_fields = ("created_at", "stripe_product_id", "stripe_price_id", "stripe_session_url")
    list_per_page = 20