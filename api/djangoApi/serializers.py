from rest_framework.serializers import ModelSerializer
from ..models import User, Room

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('userid', 'username', 'profile_photo')

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['room_code', 'created_at']

