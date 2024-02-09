from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson
from materials.serializers.lessons import LessonSerializer


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons_for_course = SerializerMethodField()

    def get_lessons_count(self, obj):
        return Lesson.objects.filter(course=obj).count()

    def get_lessons_for_course(self, obj):
        return LessonSerializer(Lesson.objects.filter(course=obj), many=True).data

    class Meta:
        model = Course
        fields = '__all__'
