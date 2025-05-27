from rest_framework.generics import CreateAPIView


from users.models import TrackerUser
from users.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = TrackerUser.objects.all()

    def perform_create(self, serializer):
        password = serializer.validated_data['password']
        user = serializer.save(is_active=True)
        user.set_password(password)
        user.save()
