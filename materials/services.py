import stripe
from private_settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def get_url_payment(course):
    product = stripe.Product.create(name=course.name)

    price = stripe.Price.create(
        currency="rub",
        unit_amount=course.price * 100,
        product_data={"name": f'Оплата курса - {product.get('name')}'},
    )

    session = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[{"price": price, "quantity": 1}],
        mode="payment",
    )

    return session.get('url')
