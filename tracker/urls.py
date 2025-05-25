from django.urls import path

from tracker.apps import TrackerConfig
from tracker.views import (HabitCreateAPIView, HabitListAPIView, HabitRetrieveAPIView, HabitUpdateAPIView,
                           HabitDestroyAPIView, PublicHabitListAPIView)

app_name = TrackerConfig.name

urlpatterns = [
    path('habit/list/', HabitListAPIView.as_view(), name='habit_list'),
    path('habit/create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('habit/<int:pk>/retrieve/', HabitRetrieveAPIView.as_view(), name='habit_retrieve'),
    path('habit/<int:pk>/update/', HabitUpdateAPIView.as_view(), name='habit_update'),
    path('habit/<int:pk>/delete/', HabitDestroyAPIView.as_view(), name='habit_destroy'),
    path('public_habits/', PublicHabitListAPIView.as_view(), name='public_habits'),
]
