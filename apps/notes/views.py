# Typs
from typing import List
# Django
from django.shortcuts import render
# Rest Framewoerk
from rest_framework.viewsets import ModelViewSet
# From App Notes
from .models import Note
from .serializer import (
        NoteSerializer,
)


class NoteViewSet(ModelViewSet):
    """ Models View Set Note """
    queryset: List[Note] = Note.objects.all()  # type: ignore
    serializer_class = NoteSerializer
