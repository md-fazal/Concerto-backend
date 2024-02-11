from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .djangoApi.urls import user_router, room_router


router = DefaultRouter()

router.registry.extend(user_router.registry)
router.registry.extend(room_router.registry)

urlpatterns = [
    path('', include(router.urls))
    
]
