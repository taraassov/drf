from rest_framework import serializers


class LinkValidator:
    def __init__(self, video_link):
        self.video_link = video_link

    def __call__(self, value):
        if (dict(value).get(self.video_link) and 'youtube.com' not in dict(value).get(self.video_link).split(
                '/')) and 'www.youtube.com' not in dict(value).get(self.video_link).split(
            '/'): raise serializers.ValidationError('The link to the video should be on youtube.com')
