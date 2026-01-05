import re

from rest_framework.exceptions import ValidationError


class YouTubeURLValidator:
    """Валидатор для проверки, что ссылка ведёт на YouTube."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if value:
            pattern = r"^https?://(www\.)?(youtube\.com|youtu\.be)/"
            if not re.match(pattern, value):
                raise ValidationError("Разрешены только ссылки на YouTube.")

    def __repr__(self):
        return f"<YouTubeURLValidator(field={self.field})>"
