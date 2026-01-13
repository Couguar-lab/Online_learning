import random
from datetime import datetime, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from lms.models import Course, Lesson
from users.models import Payment

User = get_user_model()


class Command(BaseCommand):
    """Кастомная команда для заполнения тестовыми платежами."""

    help = "Создаёт тестовые платежи для существующих пользователей, курсов и уроков."

    def handle(self, *args, **options):
        # Получаем первого пользователя (или можно расширить логику)
        try:
            user = User.objects.first()
            if not user:
                self.stdout.write(self.style.ERROR("Нет пользователей в базе."))
                return
        except:
            self.stdout.write(self.style.ERROR("Ошибка получения пользователя."))
            return

        # Получаем курсы и уроки
        courses = list(Course.objects.all())
        lessons = list(Lesson.objects.all())

        if not courses and not lessons:
            self.stdout.write(
                self.style.ERROR("Нет курсов или уроков для создания платежей.")
            )
            return

        # Создаём 5 тестовых платежей
        payment_methods = ["cash", "transfer"]
        created_count = 0

        for i in range(5):
            payment_method = random.choice(payment_methods)
            amount = Decimal(random.choice(["990.00", "1990.00", "4990.00", "6990.00"]))

            # С вероятностью 70% платёж за курс, 30% за урок
            if random.random() < 0.7 and courses:
                course = random.choice(courses)
                lesson = None
            elif lessons:
                course = None
                lesson = random.choice(lessons)
            else:
                continue

            # Дата в последние 30 дней
            days_ago = random.randint(0, 30)
            payment_date = datetime.now() - timedelta(days=days_ago)

            payment = Payment.objects.create(
                user=user,
                course=course,
                lesson=lesson,
                amount=amount,
                payment_method=payment_method,
                payment_date=payment_date,
            )

            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Успешно создано {created_count} тестовых платежей.")
        )
