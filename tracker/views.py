from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from django.db import models

from tracker.models import Tracker
from tracker.paginators import TrackerPaginator
from tracker.permissions import IsOwnerOrPublicReadOnly
from tracker.serializers import TrackerSerializer, PublicTrackerSerializer


class HabitCreateAPIView(CreateAPIView):
    serializer_class = TrackerSerializer
    permission_classes = [IsAuthenticated]
    queryset = Tracker.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.status_code = status.HTTP_201_CREATED
        return response


class HabitListAPIView(ListAPIView):
    serializer_class = TrackerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tracker.objects.filter(
            models.Q(user=self.request.user) | models.Q(is_public=True)
        )


class HabitUpdateAPIView(UpdateAPIView):
    serializer_class = TrackerSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrPublicReadOnly]
    queryset = Tracker.objects.all()


class HabitRetrieveAPIView(RetrieveAPIView):
    serializer_class = TrackerSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrPublicReadOnly]
    queryset = Tracker.objects.all()


class HabitDestroyAPIView(DestroyAPIView):
    serializer_class = TrackerSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrPublicReadOnly]
    queryset = Tracker.objects.all()


class PublicHabitListAPIView(ListAPIView):
    serializer_class = PublicTrackerSerializer
    queryset = Tracker.objects.filter(is_public=True)
    pagination_class = TrackerPaginator
    permission_classes = []
