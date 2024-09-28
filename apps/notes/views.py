# Typs
from typing import Any, List
# Rest Framewoerk
from django.contrib.auth.models import PermissionDenied
from rest_framework.views import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# From App Notes
from .models import (
        Note,
        UserNote,
)
from .serializer import (
        NoteSerializer,
        UserNoteSerializer,
        UserNoteListSerializer
        )


class NoteViewSet(ModelViewSet):
    """ Models View Set Note """
    queryset: List[Note] = Note.objects.all()  # type: ignore
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    # Asigna nota al usuario que la crea
    def create(self, request: Request) -> Response:
        """ Crea una nueva nota y la asocia al usuario autenticado. """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        note = serializer.save()
        UserNote.objects.get_or_create(user=request.user, note=note)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    #  Método list deshabilitarlo
    def list(self, request: Request, *args: Any, **kwargs: Any):
        return Response(
                {'detail': 'Método no permitido.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
                )

    # Solo puede actualizar sus notas
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:

        instance = self.get_object()

        # Verificar que la relación UserNota existe
        if not UserNote.objects.filter(
                user=request.user,
                note=instance
                ).exists():
            raise PermissionDenied(
                    'No tienes permiso para actualizar esta nota.'
                    )

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(
                instance,
                data=request.data,
                partial=partial
                )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Invalidar la caché de prefetch_related si es necesario
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class NoteUserViewSet(ModelViewSet):
    """ Model View Set For Note User"""
    queryset: List[UserNote] = UserNote.objects.filter()  # type: ignore
    serializer_class = UserNoteSerializer
    permission_classes = [IsAuthenticated]

    # Lsitamos las notas de un usuario
    def list(self, request: Request) -> Response:
        """ Listado Con Usuarios y Notas """
        queryset: List[Note] = UserNote.objects.filter(  # type: ignore
                user=request.user
                )
        serializer = UserNoteListSerializer(queryset, many=True)
        return Response(serializer.data)
