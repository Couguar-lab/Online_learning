import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_product(name):
    """Создать продукт в Stripe."""
    product = stripe.Product.create(name=name)
    return product.id

def create_price(product_id, amount):
    """Создать цену в Stripe (amount в копейках)."""
    price = stripe.Price.create(
        product=product_id,
        unit_amount=amount * 100,  # 1000 руб = 100000 копеек
        currency="rub",
        recurring={"interval": "month"},
    )
    return price.id

def create_checkout_session(price_id, success_url, cancel_url):
    """Создать сессию оплаты."""
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price": price_id,
            "quantity": 1,
        }],
        mode="subscription",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session.url