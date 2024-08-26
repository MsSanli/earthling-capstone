from django.urls import path, include
from rest_framework.routers import DefaultRouter
from earthling_api.views.user_view import UserView


router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserView, 'user')

urlpatterns = [
    path('', include(router.urls)),
]
