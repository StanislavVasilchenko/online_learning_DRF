from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from materials.models import Course
from materials.permissions import IsModerator, IsUserIsOwner
from materials.serializers.course import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['create', 'retrieve_delete']:
            self.permission_classes = [IsAuthenticated, IsUserIsOwner]
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
