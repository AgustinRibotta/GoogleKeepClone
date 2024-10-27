from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Note, UserNote, Attachment
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


"""
Serializadores para Notas
"""


class UserForNoteSerializer(serializers.ModelSerializer):
    """ Serializador User para Note """
    delete_user_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'delete_user_url']

    def get_delete_user_url(self, obj):
        request = self.context.get('request')
        return reverse(
                'usernote-detail',
                kwargs={'pk': obj.id},
                request=request)


class UserNoteForNoteSerializerNote(serializers.ModelSerializer):
    """ Serializador para User Note para Note Serialzier"""
    user = UserForNoteSerializer()

    class Meta:
        model = UserNote
        fields = ['user']


class NoteDetailSerializer(serializers.ModelSerializer):
    """ Serializer para detalles de Note """
    users = UserNoteForNoteSerializerNote(many=True, source='note_user')

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'users']


class NoteSerializer(serializers.ModelSerializer):
    """ Serializar para Note """
    class Meta:
        model = Note
        fields = '__all__'


"""
Serializadores para User Nota
"""


class AttachmentSerializer(serializers.ModelSerializer):
    """ Serializer para el archivo adjunto de las Notas relacionada a un Usuario """
   
    class Meta:
        model = Attachment
        fields = ['id', 'note', 'file_path', 'create_at']
        
    def create(self, validated_data):  
        attachment = Attachment(**validated_data)
        try:
            attachment.full_clean()  # Validar el tamaño del archivo
            attachment.save()
        except ValidationError as e:
            raise serializers.ValidationError({"detail": e.messages})
        return attachment
    

class UserForNoteUserSerializer(serializers.ModelSerializer):
    """ Serializador User para User Note """
    class Meta:
        model = User
        fields = ['id', 'username']


class AttachmentForNoteUserSerializer(serializers.ModelSerializer):
    """ Serializador Attachment para User Note """
    class Meta:
        model = Attachment
        fields = ['id', 'file_path', 'create_at']


class NoteForNoteUserSerialzier(serializers.ModelSerializer):
    """ Serializor Note para User Note """
    attachments = AttachmentForNoteUserSerializer(many=True, read_only=True)
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'attachments']


class UserNoteListSerializer(serializers.ModelSerializer):
    """ Serializer para el listado de las Notas relacionadas un Usuario """
    user = UserForNoteUserSerializer(read_only=True)
    note = NoteForNoteUserSerialzier(read_only=True)
    update_note_url = serializers.SerializerMethodField()
    delete_note_url = serializers.SerializerMethodField()
    retrieve_note_url = serializers.SerializerMethodField()

    class Meta:
        model = UserNote
        fields = [
                'user',
                'note',
                'update_note_url',
                'delete_note_url',
                'retrieve_note_url'
                ]

    def get_update_note_url(self, obj):
        request = self.context.get('request')
        return reverse(
                'note-detail',
                kwargs={'pk': obj.note.id},
                request=request)

    def get_delete_note_url(self, obj):
        request = self.context.get('request')
        return reverse(
                'note-detail',
                kwargs={'pk': obj.note.id},
                request=request)

    def get_retrieve_note_url(self, obj):
        request = self.context.get('request')
        return reverse(
                'note-detail',
                kwargs={'pk': obj.note.id},
                request=request)


class UserNoteSerializer(serializers.ModelSerializer):
    """ Serialzador par Metodo Create - Delete - Update - Retrive"""
    class Meta:
        model = UserNote
        fields = '__all__'


