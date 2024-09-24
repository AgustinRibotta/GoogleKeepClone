# Django
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models


class Note(models.Model):
    """ Model Notes """
    title = models.CharField(_("Title"), max_length=150)
    content = models.TextField(_("Content"))
    create_at = models.DateTimeField(_("Create Date"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update Date"), auto_now=True)

    class Meta:
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")

    def __str__(self) -> str:
        return f"{self.title}  {self.create_at}  {self.update_at}"


class UserNote(models.Model):
    """ Models for Notes related to a user """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("User Note")
        verbose_name_plural = _("Users Notes")

    def __str__(self) -> str:
        return f"{self.user.username} {self.note.title}"  # type: ignore


class Attachment(models.Model):
    """ Model Attachment """
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    content = models.TextField(_("Content"))
    create_at = models.DateTimeField(_("Create Date"), auto_now_add=True)

    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")

    def __str__(self) -> str:
        return f"{self.note.title} {self.create_at}"  # type: ignore


class ListItems(models.Model):
    """ Model for List the Items """
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    content = models.TextField(_("Content"))
    create_at = models.DateTimeField(_("Create Date"), auto_now_add=True)