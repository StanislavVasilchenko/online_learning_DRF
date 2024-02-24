import stripe

stripe.api_key = 'sk_test_51OnKQIBBeaQdBk1QT5YEKFYOx2kuwPmy2010AJp1sNZCfnSKzXp19ldVcJ9K1MilQ2qj2qt2sIlQJp4CFEuakTee00XqMv8KvL'


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
