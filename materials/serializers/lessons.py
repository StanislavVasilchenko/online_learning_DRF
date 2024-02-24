from rest_framework import serializers

from materials.models import Lesson
from materials.validators import LessonValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LessonValidator(
            field='video_url'
        )
        ]


class LessonsSerializerForUser(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        exclude = ['id', 'user']
