from rest_framework.viewsets import ModelViewSet
from ..models import User, Room
from .serializers import UserSerializer, RoomSerializer
from rest_framework.views import APIView

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer