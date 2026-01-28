from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Course, Subscription


@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(id=course_id)
    subscribers = Subscription.objects.filter(course_id=course_id)

    for sub in subscribers:
        send_mail(
            subject=f"Обновление в курсе: {course.title}",
            message=f"В курсе '{course.title}' появились новые материалы!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[sub.user.email],
            fail_silently=False,
        )

@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(id=course_id)

    # Проверяем, обновлялся ли курс менее 4 часов назад
    from datetime import timedelta
    from django.utils import timezone

    if course.updated_at > timezone.now() - timedelta(hours=4):
        return  # не отправляем, если недавно обновлялся

    subscribers = Subscription.objects.filter(course_id=course_id)
    for sub in subscribers:
        send_mail(
            subject=f"Обновление в курсе: {course.title}",
            message=f"В курсе '{course.title}' появились новые материалы!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[sub.user.email],
            fail_silently=False,
        )