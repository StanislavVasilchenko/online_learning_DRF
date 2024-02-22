from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson, Subscription
from materials.serializers.lessons import LessonSerializer


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons_for_course = SerializerMethodField()
    subscription = SerializerMethodField()

    def get_lessons_count(self, obj):
        return Lesson.objects.filter(course=obj).count()

    def get_lessons_for_course(self, obj):
        return LessonSerializer(Lesson.objects.filter(course=obj), many=True).data

    def get_subscription(self, obj):
        subscription = Subscription.objects.filter(course=obj.id, user=obj.user)
        if subscription:
            return True
        return False

    class Meta:
        model = Course
        fields = '__all__'
