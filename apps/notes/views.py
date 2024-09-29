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
    queryset: List[Note] = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request: Request) -> Response:
        """ Crea una nueva nota y la asocia al usuario autenticado. """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        note = serializer.save()
        UserNote.objects.get_or_create(user=request.user, note=note)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request: Request, *args: Any, **kwargs: Any):
        """ Metodo list deshabilitarlo"""
        return Response(
                {'detail': 'Método no permitido.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
                )

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """ Metodo para actualizar solo las Notas del Usuario """
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

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """ Metodo para ver los detalles solo las Notas del Usuario """
        instance = self.get_object()

        if not UserNote.objects.filter(
                user=request.user,
                note=instance).exists():
            raise PermissionDenied(
                    'No tienes permiso para ver esta nota.'
                    )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request: Request, *args: Any, **kwargs: Any):
        """ Metodo para elimianar solo las Notas del Usuario """
        instance = self.get_object()

        # Verificar que la relación UserNota existe
        if not UserNote.objects.filter(
                user=request.user,
                note=instance
                ).exists():
            raise PermissionDenied(
                    'No tienes permiso para eliminar esta nota.'
                    )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class NoteUserViewSet(ModelViewSet):
    """ Model View Set For Note User"""
    queryset: List[UserNote] = UserNote.objects.filter()
    serializer_class = UserNoteSerializer
    permission_classes = [IsAuthenticated]

    # Litamos las notas de un usuario
    def list(self, request: Request) -> Response:
        """ Listado Con Usuarios y Notas """
        queryset: List[Note] = UserNote.objects.filter(
                user=request.user
                )
        serializer = UserNoteListSerializer(queryset, many=True)
        return Response(serializer.data)
