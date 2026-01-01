from rest_framework.exceptions import ValidationError
import re


def validate_youtube_url(value):
    """Валидатор: разрешает только ссылки на youtube.com."""
    if value is None:
        return

    pattern = r'^https?://(www\.)?(youtube\.com|youtu\.be)/'
    if not re.match(pattern, value):
        raise ValidationError('Разрешены только ссылки на YouTube.')