from rest_framework import routers
from .views import NoteViewSet

router = routers.DefaultRouter()

router.register(r'note', NoteViewSet)

urlpatterns = router.urls
