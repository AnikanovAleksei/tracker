from rest_framework import serializers

from users.models import TrackerUser


class UserSerializer(serializers.ModelSerializer):
    model = TrackerUser
    fields = "__all__"
