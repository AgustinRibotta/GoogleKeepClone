from rest_framework import serializers
from .models import Note, UserNote, Attachment, ListItems


class NoteSerializer(serializers.ModelSerializer):
    """ Serializer for Note """
    class Meta:
        model = Note
        fields = '__all__'


class UserNoteSerializer(serializers.ModelSerializer):
    """ Serializer for User Note """
    class Meta:
        model = UserNote
        fields = '__all__'


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
