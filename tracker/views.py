from datetime import timedelta
from django.utils import timezone
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from django.db import models

from tracker.models import Tracker
from tracker.paginators import TrackerPaginator
from tracker.serializers import TrackerSerializer, PublicTrackerSerializer
from rest_framework.response import Response
from tracker.tasks import check_and_send_reminders


class HabitCreateAPIView(CreateAPIView):
    serializer_class = TrackerSerializer
    permission_classes = [IsAuthenticated]
    queryset = Tracker.objects.all()

    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user)

        # Устанавливаем первое напоминание
        habit.next_reminder = timezone.now() + timedelta(minutes=10)  # Для теста
        habit.save()

        # Запускаем фоновую проверку
        check_and_send_reminders.delay()

        return Response({"status": "Habit created and reminders scheduled"})


class HabitListAPIView(ListAPIView):
    serializer_class = TrackerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TrackerPaginator

    def get_queryset(self):
        return Tracker.objects.filter(
            models.Q(user=self.request.user) | models.Q(is_public=True)
        )


class HabitUpdateAPIView(UpdateAPIView):
    serializer_class = TrackerSerializer
    pagination_class = TrackerPaginator

    def get_queryset(self):
        return Tracker.objects.filter(user=self.request.user)


class HabitRetrieveAPIView(RetrieveAPIView):
    serializer_class = TrackerSerializer
    pagination_class = TrackerPaginator

    def get_queryset(self):
        return Tracker.objects.filter(user=self.request.user)


class HabitDestroyAPIView(DestroyAPIView):
    serializer_class = TrackerSerializer
    pagination_class = TrackerPaginator

    def get_queryset(self):
        return Tracker.objects.filter(user=self.request.user)


class PublicHabitListAPIView(ListAPIView):
    serializer_class = PublicTrackerSerializer
    queryset = Tracker.objects.filter(is_public=True)
    pagination_class = TrackerPaginator
    permission_classes = []
