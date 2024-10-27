# Django
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError


class Note(models.Model):
    """ Model Notes """
    title = models.CharField(_("Title"), max_length=150)
    content = models.TextField(_("Content"), blank=True, null=True)
    create_at = models.DateTimeField(_("Create Date"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update Date"), auto_now=True)

    class Meta:
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")

    def __str__(self) -> str:
        return f"{self.title}"


class UserNote(models.Model):
    """ Models for Notes related to a user """
    user = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            related_name='user_note'
            )
    note = models.ForeignKey(
            Note,
            on_delete=models.CASCADE,
            related_name='note_user'
            )

    class Meta:
        verbose_name = _("User Note")
        verbose_name_plural = _("Users Notes")

    def __str__(self) -> str:
        return f"{self.user.username} {self.note.title}"  # type: ignore


class Attachment(models.Model):
    """ Model Attachment """
    note = models.ForeignKey(Note, related_name='attachments', on_delete=models.CASCADE)
    file_path = models.FileField(_("File Path"), upload_to='attachments/', null=True)  #I associate the flie_path variable with the media folder
    create_at = models.DateTimeField(_("Create Date"), auto_now_add=True)

    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")

    def __str__(self) -> str:
        return f"{self.note.title} {self.create_at}"  
    
    def clean(self):  #I create a clean method to validate the size of the file
        max_file_size = 5 * 1024 * 1024  # 5MB
        if self.file_path and self.file_path.size>max_file_size:
            raise ValidationError(('File size cannot exceed 5MB'))
        


class ListItems(models.Model):
    """ Model for List the Items """
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    content = models.TextField(_("Content"))
    create_at = models.DateTimeField(_("Create Date"), auto_now_add=True)

    class Meta:
        verbose_name = _("List Item")
        verbose_name_plural = _("List Items")

    def __str__(self) -> str:
        return f"{self.note.title} {self.create_at}"
