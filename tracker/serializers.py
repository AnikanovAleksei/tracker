from rest_framework import serializers

from tracker.models import Tracker


class TrackerSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Tracker
        fields = '__all__'


class PublicTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracker
        fields = ['id', 'place', 'action', 'duration', 'periodicity']
        read_only_fields = fields
