from rest_framework import routers
from .views import (
        NoteViewSet,
        NoteUserViewSet,
        )

router = routers.DefaultRouter()

router.register(r'note', NoteViewSet)
router.register(r'user-note', NoteUserViewSet)

urlpatterns = router.urls
