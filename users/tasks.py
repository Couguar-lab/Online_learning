from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

@shared_task
def block_inactive_users():
    """Блокирует пользователей, не заходивших более месяца."""
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(
        last_login__lt=one_month_ago,
        is_active=True
    )
    count = inactive_users.update(is_active=False)
    print(f"Заблокировано {count} неактивных пользователей")