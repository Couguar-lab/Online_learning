import stripe
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Payment
from .permissions import IsOwner
from .serializers import PaymentSerializer, RegisterSerializer, UserSerializer
from .services import create_product, create_price, create_checkout_session
from django.urls import reverse

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(
        detail=False, methods=["get", "patch"], permission_classes=[IsAuthenticated], url_path='me', url_name='me'
    )
    def me(self, request):
        """Эндпоинт /me/ — текущий пользователь."""
        if request.method == "GET":
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method == "PATCH":
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    def get_permissions(self):
        """Запрет редактирования чужого профиля."""
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]


class PublicUserSerializer(serializers.ModelSerializer):
    """Публичный профиль без чувствительных данных."""

    class Meta:
        model = User
        fields = ("id", "email", "phone", "city", "avatar", "date_joined")


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет платежей с фильтрацией и сортировкой."""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["course", "lesson", "payment_method"]
    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]


class RegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя."""

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class CreatePaymentView(APIView):
    """Создать платеж и получить ссылку на оплату."""

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save(user=request.user)

        # Создать продукт и цену в Stripe
        product_id = create_product(payment.course.title)
        price_id = create_price(product_id, payment.amount)

        # Сохранить Stripe ID
        payment.stripe_product_id = product_id
        payment.stripe_price_id = price_id

        # Создать сессию оплаты
        success_url = request.build_absolute_uri(reverse('payment-success'))
        cancel_url = request.build_absolute_uri(reverse('payment-cancel'))
        session_url = create_checkout_session(price_id, success_url, cancel_url)

        payment.stripe_session_url = session_url
        payment.save()

        return Response({
            'payment_id': payment.id,
            'session_url': session_url
        }, status=status.HTTP_201_CREATED)

class CheckPaymentStatus(APIView):
    def get(self, request, payment_id):
        try:
            payment = Payment.objects.get(id=payment_id, user=request.user)
            session = stripe.checkout.Session.retrieve(payment.stripe_session_id)
            return Response({"status": session.payment_status})
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found or not yours"}, status=status.HTTP_404_NOT_FOUND)
        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)