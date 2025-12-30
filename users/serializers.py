from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Payment

User = get_user_model()


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор платежа."""

    user = serializers.StringRelatedField()
    course = serializers.StringRelatedField(allow_null=True)
    lesson = serializers.StringRelatedField(allow_null=True)

    class Meta:
        model = Payment
        fields = (
            "id",
            "user",
            "payment_date",
            "course",
            "lesson",
            "amount",
            "payment_method",
        )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя с историей платежей."""

    payments = PaymentSerializer(many=True, read_only=True, source="payments")

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone",
            "city",
            "avatar",
            "date_joined",
            "last_login",
            "payments",
        )
        read_only_fields = ("id", "date_joined", "last_login", "payments")


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "phone", "city")

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            phone=validated_data.get("phone"),
            city=validated_data.get("city"),
        )
        return user
