from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course
from materials.paginators import LessonsAndCoursePaginator
from materials.permissions import IsModerator, IsUserIsOwner
from materials.serializers.course import CourseSerializer
from materials.services import get_url_payment
from users.models import Payment


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = LessonsAndCoursePaginator

    def get_permissions(self):
        if self.action in ['create', 'retrieve_delete']:
            self.permission_classes = [IsAuthenticated, IsUserIsOwner, ~IsModerator]
        else:
            self.permission_classes = [IsAuthenticated, IsUserIsOwner | IsModerator]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.queryset.filter(user=self.request.user).exists():
            return Course.objects.filter(user=self.request.user)
        elif self.request.user.is_superuser or self.request.user.groups.filter(name='moderator').exists():
            return self.queryset


class CoursePaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")

        item = get_object_or_404(Course, pk=course_id)
        if item:
            payment_url = get_url_payment(item)

            payment = Payment.objects.create(user=user,
                                             course=item,
                                             amount=item.price
                                             )
            payment.save()
            return Response({"url": payment_url})
        return Response({"error": "Payment does not exist."}, status=status.HTTP_400_BAD_REQUEST)
