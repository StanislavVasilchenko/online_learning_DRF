from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics

from users.models import Payment, User
from users.serializers.payment import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('course', 'lesson', 'method')
