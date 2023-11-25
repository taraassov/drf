from django.urls import path

from tutorial.apps import TutorialConfig
from rest_framework.routers import DefaultRouter

from tutorial.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentListAPIView, SubscribeCreateAPIView, SubscribeDestroyAPIView, \
    SubscribeListAPIView, PaymentCreateAPIView, PaymentRetrieveAPIView

app_name = TutorialConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),

    # payment
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('payment/', PaymentListAPIView.as_view(), name='payment-list'),
    path('payment/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment-get'),

    # subscription
    path('subscribe/create/', SubscribeCreateAPIView.as_view(), name='subscribe-create'),
    path('subscribe/', SubscribeListAPIView.as_view(), name='subscribe-list'),
    path('subscribe/delete/<int:pk>/', SubscribeDestroyAPIView.as_view(), name='subscribe-delete')
] + router.urls
