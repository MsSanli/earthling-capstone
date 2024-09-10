from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from earthling_api.views import UserView, EntryView, SubjectView, LanguageView, TagView, check_user, register_user


# notes: The first argument is what you want your URL path to be.
# The second argument is the view that will handle client requests to that route.
# The third argument is needed in order for a route to be registered
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserView, 'user')
router.register(r'entries', EntryView, 'entry')
router.register(r'subjects', SubjectView, 'subject')
router.register(r'languages', LanguageView, 'language')
router.register(r'tags', TagView, 'tag')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('register', register_user),
    path('checkuser', check_user),
]
