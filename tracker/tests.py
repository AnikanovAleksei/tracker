from django.test import TestCase
from django.core.exceptions import ValidationError
from tracker.models import Tracker
from users.models import TrackerUser
from tracker.serializers import TrackerSerializer, PublicTrackerSerializer


class TrackerModelTest(TestCase):
    def setUp(self):
        self.user = TrackerUser.objects.create(username="testuser", tg_id_chat=12356)
        self.habit = Tracker.objects.create(
            user=self.user,
            action="Test action",
            place="Test place",
            periodicity=7,
            duration=30
        )
        self.habit_data = {
            "action": "New habit",
            "place": "Home",
            "periodicity": 7,
            "duration": 60
        }

    def test_habit_creation(self):
        self.assertEqual(self.habit.action, "Test action")
        self.assertEqual(self.habit.periodicity, 7)

    def test_pleasant_habit_validation(self):
        pleasant_habit = Tracker(
            user=self.user,
            action="Pleasant",
            is_pleasant=True,
            reward="Invalid reward",
            periodicity=7
        )
        with self.assertRaises(ValidationError):
            pleasant_habit.full_clean()

    def test_related_habit_validation(self):
        main_habit = Tracker.objects.create(
            user=self.user,
            action="Main",
            is_pleasant=False,
            periodicity=7
        )
        with self.assertRaises(ValidationError):
            main_habit.related_habit = self.habit
            main_habit.full_clean()

    def test_create_habit(self):
        request = self.client.get('/')
        request.user = self.user

        serializer = TrackerSerializer(data=self.habit_data, context={'request': request})
        self.assertTrue(serializer.is_valid())
        habit = serializer.save(user=self.user)
        self.assertEqual(habit.action, "New habit")

    def test_public_serializer_fields(self):
        serializer = PublicTrackerSerializer()
        self.assertEqual(
            list(serializer.fields.keys()),
            ['id', 'place', 'action', 'duration', 'periodicity']
        )
