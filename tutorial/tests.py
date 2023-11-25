from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from tutorial.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@example.com', is_active=True)
        self.user.set_password('test_password')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Test Course', description='This is a test course')
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='This is a test lesson',
            course=self.course,
            owner=self.user,
            video_link='https://www.youtube.com/watch?v=49HZiaGu298&ab_channel=TRUEGYMMMA'
        )

    def test_get_lesson(self):
        """ Test Lesson List """

        response = self.client.get(
            reverse('tutorial:lesson-list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        print(response.json())

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson.id,
                        "title": self.lesson.title,
                        "description": self.lesson.description,
                        "preview": None,
                        "video_link": self.lesson.video_link,
                        "course": self.lesson.course_id,
                        "owner": self.lesson.owner_id,
                    }
                ]
            }
        )

    def test_create_lesson(self):
        """ Test Create Lesson """

        data = {
            # "id": 2,
            "title": "Test Lesson1",
            "description": "This is a test lesson1",
            # "video_link": 'https://www.youtube.com/watch?v=XQ94dUE&ab',
            "course": self.course.id
            # "owner": 1
        }

        response = self.client.post(
            reverse('tutorial:lesson-create'),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_update_lesson(self):
        """ Test Update Lesson """
        data = {
            "title": "Updated Test Lesson",
            "description": "This is an updated test lesson",
            "course": self.course.id,
            "owner": self.user.id
        }
        response = self.client.put(
            reverse('tutorial:lesson-update', kwargs={'pk': self.lesson.id}),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        """ Test Delete Lesson """
        response = self.client.delete(
            reverse('tutorial:lesson-delete', kwargs={'pk': self.lesson.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com', is_active=True)
        self.user.set_password('test_password')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Test Course', description='This is a test course')

    def test_create_subscription(self):
        """ Test Create Subscription """

        data = {
            "course": self.course.id,
            "user": self.user.id,
            "is_active": True
        }

        response = self.client.post(
            reverse('tutorial:subscribe-create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_subscription(self):
        """ Test List Subscription """

        Subscription.objects.create(course=self.course, user=self.user)

        response = self.client.get(
            reverse('tutorial:subscribe-list')
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_subscription(self):
        """ Test Delete Subscription """

        subscription = Subscription.objects.create(course=self.course, user=self.user)

        response = self.client.delete(
            reverse('tutorial:subscribe-delete', kwargs={'pk': subscription.id})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


