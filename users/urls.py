from django.http import HttpResponse
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet, RegisterView, UserViewSet, CreatePaymentView, CheckPaymentStatus

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"payments", PaymentViewSet, basename="payment")

app_name = "users"

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
    path('payment/create/', CreatePaymentView.as_view(), name='payment-create'),
    path('payment/success/', lambda request: HttpResponse("Оплата успешна"), name='payment-success'),
    path('payment/cancel/', lambda request: HttpResponse("Оплата отменена"), name='payment-cancel'),
    path('payment/check/<int:payment_id>/', CheckPaymentStatus.as_view(), name='payment-check'),
]
