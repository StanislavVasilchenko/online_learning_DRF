from rest_framework import viewsets

from materials.models import Course
from materials.permissions import IsModerator
from materials.serializers.course import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action == 'partial_update' or self.action == 'update':
            self.permission_classes = [IsModerator]
        return [permission() for permission in self.permission_classes]
