from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViews, ConversationViews

router = DefaultRouter()
router.register(r'message', MessageViews)
router.register(r'conversation', ConversationViews)
urlpatterns = [
    path('', include(router.urls))
]
