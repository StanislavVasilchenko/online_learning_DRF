import stripe
from private_settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_product(amount, prod_name):
    stripe.Product.create(name=prod_name)

    price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": prod_name},
    )
    return price


def create_session(price):
    session = stripe.checkout.Session.create(
        success_url="http://localhost:8000/materials/",
        line_items=[{"price": price, "quantity": 1}],
        mode="payment",
    )

    return session
