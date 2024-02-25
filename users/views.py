from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from materials.models import Course
from users.models import Payment, User
from users.serializers.payment import PaymentSerializer
from users.serializers.users import UserSerializer
from users.services import create_product, create_session


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'method')
    ordering_fields = ('date',)

    def create(self, request, *args, **kwargs):
        product = get_object_or_404(Course, pk=request.data.get('course'))
        if product:
            price = create_product(product.price, product.name)
            session = create_session(price)
            session_id = session.id
            session_url = session.url
            payment = Payment.objects.create(
                user=self.request.user,
                course=product,
                lesson=request.data.get('lesson'),
                amount=product.price,
                session_id=session_id,
                pay_url=session_url,
            )
            payment.save()
            return Response({"payment_url": payment.pay_url}, status=status.HTTP_201_CREATED)
        return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create(
                email=request.data['email'],
            )
            user.set_password(request.data['password'])
            user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
