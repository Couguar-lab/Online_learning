from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Payment

User = get_user_model()


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор платежа."""
    user = serializers.StringRelatedField()
    course = serializers.StringRelatedField(allow_null=True)
    lesson = serializers.StringRelatedField(allow_null=True)

    class Meta:
        model = Payment
        fields = ('id', 'user', 'payment_date', 'course', 'lesson', 'amount', 'payment_method')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя с историей платежей."""
    payments = PaymentSerializer(many=True, read_only=True, source='payments')

    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'city', 'avatar', 'date_joined', 'last_login', 'payments')
        read_only_fields = ('id', 'date_joined', 'last_login', 'payments')