from rest_framework import serializers
from .models import Note, UserNote, Attachment, ListItems
from django.contrib.auth.models import User


class NoteSerializer(serializers.ModelSerializer):
    """ Serializer para Note """
    class Meta:
        model = Note
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    """ Serializador User para User Note """
    class Meta:
        model = User
        fields = ['username']


class UserNoteSerializer(serializers.ModelSerializer):
    """ Serializer para las Notas relacionadas un Usuario """
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = UserNote
        fields = ['user', 'note']


class AttachmentSerializer(serializers.ModelSerializer):
    """ Serializer for Attachment """
    class Meta:
        model = Attachment
        fields = '__all__'


class ListItemsSerializer(serializers.ModelSerializer):
    """ Serializer for List Items """
    class Meta:
        model = ListItems
        fields = '__all__'
