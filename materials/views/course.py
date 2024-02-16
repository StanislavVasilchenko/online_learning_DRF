from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from materials.models import Course
from materials.permissions import IsModerator, IsUserIsOwner, IsStaff
from materials.serializers.course import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsUserIsOwner]
        else:
            self.permission_classes = [IsAuthenticated, IsStaff]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


