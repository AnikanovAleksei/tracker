from rest_framework import serializers

from users.models import TrackerUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = TrackerUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'city', 'avatar', 'password']
