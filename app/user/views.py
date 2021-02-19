from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User

from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny, )
