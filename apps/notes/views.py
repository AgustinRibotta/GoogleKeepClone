# Typs
from typing import List
# Rest Framewoerk
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
        UserNoteSerializer
        )


class NoteViewSet(ModelViewSet):
    """ Models View Set Note """
    queryset: List[Note] = Note.objects.all()  # type: ignore
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request: Request) -> Response:
        """ Crea una nueva nota y la asocia al usuario autenticado. """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        note = serializer.save()
        UserNote.objects.get_or_create(user=request.user, note=note)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NoteUserViewSet(ModelViewSet):
    """ Model View Set For Note User"""
    queryset: List[UserNote] = UserNote.objects.all()  # type: ignore
    serializer_class = UserNoteSerializer
