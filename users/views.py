from rest_framework import viewsets

from users.models import Payment, User
from users.serializers.payment import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

