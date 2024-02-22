from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.reverse import reverse

from materials.models import Course, Lesson
from users.models import User
from rest_framework.test import APITestCase


class LessonsTestCase(APITestCase):
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

    def test_add_lesson_validation_error(self):
        """Тест ошибки валидации video_url"""
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse('materials:lessons_create'),
            data={'course': self.course.id,
                  'name': self.lesson.name,
                  'user': self.user.id,
                  'video_url': 'https://www.rutube.com'
                  }
        )

        self.assertEqual(response.json(),
                         {'non_field_errors': ['YouTube video only']})

    def test_add_lesson_moderator(self):
        """Тест создания урока если пользователь входит в группу модераторов"""
        self.user.groups.add(Group.objects.create(name='moderator'))
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse('materials:lessons_create'),
            data={'course': self.course.id,
                  'name': self.lesson.name,
                  'user': self.user.id,
                  'video_url': 'https://www.youtube.com'
                  }
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(),
                         {'detail': 'У вас недостаточно прав для выполнения данного действия.'})

    def test_detail_lesson(self):
        """Тест вывода деталей урока если пользователь является создателем урока"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('materials:lessons_detail', args=[self.lesson.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_lesson_error(self):
        """Тест ошибки вывода деталей урока, если пользователь не является создателем"""
        self.client.force_authenticate(user=self.user)

        self.user = User.objects.create(
            email='test2@local.ru',
            password='54321'
        )

        self.lesson = Lesson.objects.create(
            course=self.course,
            name='test2',
            user=self.user,
        )

        response = self.client.get(
            reverse('materials:lessons_detail', kwargs={'pk': self.lesson.pk}),
        )

        self.assertEqual(response.json(),
                         {'detail': 'У вас недостаточно прав для выполнения данного действия.'})

    def test_detail_lesson_moderator(self):
        """Тест для вывода любого урока если пользователь состоит в группе модераторов"""
        self.user.groups.add(Group.objects.create(name='moderator'))
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('materials:lessons_detail', args=[self.lesson.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        """Тест обновления урока, если пользователь является создателем"""

        self.client.force_authenticate(user=self.user)

        data = {'name': 'testlesson2'}
        response = self.client.put(reverse('materials:lessons_update', args=[self.lesson.id]),
                                   data=data
                                   )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json().get('name'), 'testlesson2')

    def test_update_lesson_moderator(self):
        """Тест изменения урока модератором"""
        self.user.groups.add(Group.objects.create(name='moderator'))
        self.client.force_authenticate(user=self.user)

        data = {'name': 'test for moderator'}
        response = self.client.put(reverse('materials:lessons_update', args=[self.lesson.id]),
                                   data=data
                                   )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json().get('name'), 'test for moderator')

    def test_update_lesson_error(self):
        """Тест для обновления урока если пользователь не является создателем
         или не состоит в группе модераторов"""

        self.client.force_authenticate(user=self.user)

        self.user = User.objects.create(
            email='test2@local.ru',
            password='54321'
        )

        self.lesson = Lesson.objects.create(
            course=self.course,
            name='test2',
            user=self.user,
        )

        data = {'name': 'fail data'}

        response = self.client.put(reverse('materials:lessons_update', args=[self.lesson.id]),
                                   data=data
                                   )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(response.json().get('detail'),
                         'У вас недостаточно прав для выполнения данного действия.')

    def test_delete_lesson(self):
        """Тест удаления урока"""
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(reverse('materials:lessons_delete', args=[self.lesson.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_lessons_list(self):
        """Тест на получения списка уроков"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('materials:lessons_list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Lesson.objects.count(), 1)

    def test_subscription_create_or_delete(self):
        """Тест подписки на обновление кураса"""
        self.client.force_authenticate(user=self.user)

        response = self.client.post(reverse('materials:subscription'),
                                    {'course': self.course.id,
                                     'user': self.user.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json().get('message'), "Subscription created")

        response = self.client.post(reverse('materials:subscription'),
                                    {'course': self.course.id,
                                     'user': self.user.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json().get('message'), "Subscription delete")
