from rest_framework import routers
from .views import (
        NoteViewSet,
        NoteUserViewSet,
        AttachmentViewSet
        )

router = routers.DefaultRouter()

router.register(r'note', NoteViewSet)
router.register(r'user-note', NoteUserViewSet, basename='user-note')
router.register(r'attachment', AttachmentViewSet, basename='attachment') 

urlpatterns = router.urls
