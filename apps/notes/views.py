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
        Attachment
)
from .serializer import (
        NoteSerializer,
        UserNoteListSerializer,
        NoteDetailSerializer,
        UserNoteSerializer, AttachmentSerializer
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
        serializer = NoteDetailSerializer(instance)
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
    queryset: List[UserNote] = UserNote.objects.all()
    serializer_class = UserNoteSerializer
    permission_classes = [IsAuthenticated]

    # Litamos las notas de un usuario
    def list(self, request: Request) -> Response:
        """ Listado Con Usuarios y Notas """
        queryset: List[Note] = UserNote.objects.filter(
                user=request.user
                )
        serializer = UserNoteListSerializer(
                queryset,
                many=True,
                context={'request': request}
                )
        return Response(serializer.data)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        note_id = request.data.get('note')

        # Verifica si el usuario puede agregar a alguien a la nota
        if not UserNote.objects.filter(user=request.user, note_id=note_id).exists():
            raise PermissionDenied('No tienes permiso para agregar usuarios a esta nota')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'El usuario fue agregado con éxito',
        }, status=status.HTTP_200_OK)

    def update(self, request: Request, *arg: Any, **kwargs: Any) -> Response:
        return Response(
            {'detail': 'Método no permitido.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

    def retrieve(self, request: Request, *arg: Any, **kwargs: Any) -> Response:
        return Response(
            {'detail': 'Método no permitido.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        usernote = self.get_object()

        if usernote.user != request.user:
            raise PermissionDenied('No tienes permiso para eliminar a este usuario de esta nota')

        usernote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AttachmentViewSet(ModelViewSet):
    """ ViewSet para manejar los archivos adjuntos """
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_notes = UserNote.objects.filter(user=user).values_list('note', flat=True)
        return Attachment.objects.filter(note__in=user_notes)

    def perform_create(self, serializer):
        note_id = self.request.data.get('note')

        # Asegurarse de que la nota existe
        try:
            note = Note.objects.get(id=note_id)
        except Note.DoesNotExist:
            return Response({"detail": "La nota no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Verificar que la nota pertenece al usuario autenticado
        if not UserNote.objects.filter(note=note, user=self.request.user).exists():
            return Response({"detail": "No tienes permiso para adjuntar archivos a esta nota."}, status=status.HTTP_403_FORBIDDEN)

        # Guardar el adjunto
        serializer.save(note=note)

    def perform_update(self, serializer):
        # Obtener el adjunto a modificar
        attachment = self.get_object()

        # Verificar que el adjunto pertenece al usuario
        if not UserNote.objects.filter(note=attachment.note, user=self.request.user).exists():
            return Response({"detail": "No tienes permiso para modificar este adjunto."}, status=status.HTTP_403_FORBIDDEN)

        # Guardar los cambios
        serializer.save()

    def perform_destroy(self, instance):
        # Verificar que el adjunto pertenece al usuario
        if not UserNote.objects.filter(note=instance.note, user=self.request.user).exists():
            return Response({"detail": "No tienes permiso para eliminar este adjunto."}, status=status.HTTP_403_FORBIDDEN)

        # Eliminar el adjunto
        instance.delete()