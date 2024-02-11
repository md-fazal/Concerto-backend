#  NO SERIALIZER BECAUSE THE MODEL IS READ ONLY AND CAN BE WRITTEN ONLY AT BACKEND

# from rest_framework.serializers import ModelSerializer
# from .models import SpotifyToken

# class TokenSerializer(ModelSerializer):
#     class Meta:
#         model = SpotifyToken
#         fields = '__all__'
#         read_only_fields = ['created_at']