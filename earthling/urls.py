from django.urls import path, include
from rest_framework.routers import DefaultRouter
from earthling_api.views import UserView, EntryView, SubjectView, LanguageView

# notes: The first argument is what you want your URL path to be.
# The second argument is the view that will handle client requests to that route.
# The third argument is needed in order for a route to be registered
router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserView, 'user')
router.register(r'entry', EntryView, 'entry')
router.register(r'subject', SubjectView, 'subject')
router.register(r'language', LanguageView, 'language')

urlpatterns = [
    path('', include(router.urls)),
]
