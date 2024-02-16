from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from materials.models import Lesson
from materials.permissions import IsModerator, IsUserIsOwner
from materials.serializers.lessons import LessonSerializer, LessonsSerializerForUser


class LessonsListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsUserIsOwner]

    def get_queryset(self):
        if Lesson.objects.filter(user=self.request.user).exists():
            self.serializer_class = LessonsSerializerForUser
            return Lesson.objects.filter(user=self.request.user)
        elif self.request.user.groups.filter(name='moderator').exists() or self.request.user.is_staff:
            return Lesson.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LessonDetailAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsUserIsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsUserIsOwner]


class LessonDeleteAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsUserIsOwner]
