from rest_framework import generics
from users.serializers import UserSeralizer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSeralizer
