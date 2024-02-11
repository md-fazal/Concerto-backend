from django.urls import path
from .views import RoomViewSet, UserViewSet
from rest_framework.routers import DefaultRouter

user_router = DefaultRouter()
user_router.register(r'users', UserViewSet)

room_router = DefaultRouter()
room_router.register(r'rooms', RoomViewSet)

