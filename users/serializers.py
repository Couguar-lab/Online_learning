from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "phone", "city", "avatar", "date_joined", "last_login")
        read_only_fields = ("id", "date_joined", "last_login")

    # Для обновления пароля (опционально)
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)
