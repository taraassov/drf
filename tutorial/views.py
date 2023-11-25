from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from tutorial.models import Course, Lesson, Payment, Subscription
from tutorial.paginators import LessonPaginator
from tutorial.permissions import IsNotStaffUser, IsOwnerOrStaff
from tutorial.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer
from tutorial.services import get_session

from tutorial.tasks import send_course_update_email

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = LessonPaginator

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated, IsNotStaffUser]
        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsAuthenticated, IsOwnerOrStaff]
        elif self.action == "destroy":
            permission_classes = [IsAuthenticated, IsNotStaffUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Course.objects.filter(owner=self.request.user)
        elif self.request.user.is_staff:
            return Course.objects.all()
        else:
            raise PermissionDenied


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsNotStaffUser]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LessonPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaff]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaff]

    def perform_update(self, serializer):
        instance = serializer.save()
        course = instance.course
        subscriptions = Subscription.objects.filter(course=course, is_active=True)
        for subscription in subscriptions:
            user_email = subscription.user.email
            send_course_update_email.delay(user_email, course.title)


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsNotStaffUser]


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        course = serializer.validated_data.get('course')
        if not course:
            raise serializers.ValidationError('Курс не указан.')
        payment = serializer.save()
        payment.user = self.request.user
        session_url = get_session(payment)  # Получаем URL сессии
        payment.session = session_url  # Сохраняем URL сессии
        payment.save()


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ('-date',)


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class SubscribeCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class SubscribeListAPIView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubscribeDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
