from rest_framework import status
from rest_framework.reverse import reverse

from materials.models import Course, Lesson
from users.models import User
from rest_framework.test import APITestCase


class MaterialsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@local.ru',
            password='12345'
        )

        self.course = Course.objects.create(
            name='testcourse',
            user=self.user
        )

        self.lesson = Lesson.objects.create(
            name='testlesson',
            course=self.course,
            user=self.user
        )

    def test_add_lesson(self):
        """Тест создания урока"""

        self.client.force_authenticate(user=self.user)

        data = {'course': self.course.id,
                'name': self.lesson.name,
                'user': self.user.id,
                'video_url': 'https://www.youtube.com/'
                }


        response = self.client.post(
            reverse('materials:lessons_create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data['video_url'] = 'https://www.rutube.com/'
        response = self.client.post(
            reverse('materials:lessons_create'),
            data=data
        )

        self.assertEqual(response.json(),
                         {'non_field_errors': ['YouTube video only']})


