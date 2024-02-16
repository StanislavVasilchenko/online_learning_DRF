from rest_framework import serializers

from materials.models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class LessonsSerializerForUser(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        exclude = ['id', 'user']


