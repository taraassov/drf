# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from tutorial.models import Course, Lesson, Payment, Subscription
from tutorial.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    validators = [LinkValidator(video_link='video_link')]
    # def validate(self, data):
    #     print(data.__dict__)
    #     if 'www.youtube.com' not in data['video_link'].split('/'):
    #         raise ValidationError('Only links to YouTube videos are allowed.')
    #     return data

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    # num_lessons = serializers.IntegerField(source='lesson_set.count', read_only=True)
    num_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    is_subscribed = serializers.SerializerMethodField()

    def get_num_lessons(self, obj):
        return Lesson.objects.all().filter(course=obj).count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            subscription = Subscription.objects.filter(course=obj, user=user).first()
            if subscription:
                return subscription.is_active
        return False

    class Meta:
        model = Course
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('id', 'course', 'user', 'is_active')

