from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import hashlib

import managers


class BaseModel(models.Model):
    created_at = models.DateTimeField(_(u'Created At'), auto_now_add=True, )
    updated_at = models.DateTimeField(_(u'Updated At'), auto_now=True, )

    class Meta:
        abstract = True


class Token(BaseModel):
    user = models.ForeignKey(User)
    token_type = models.CharField(
        _('Token Type'), max_length=20, default='Bearer')
    token_value = models.TextField(_('Token Value'))
    token_digest = models.CharField(
        _('Token digest'), max_length=50, unique=True)

    class Meta:
        verbose_name = _('Token')
        verbose_name_plural = _('Token')

    objects = managers.TokenQuerySet.as_manager()

    @classmethod
    def digest(cls, value):
        return hashlib.sha256(value).hexdigest()

    def save(self, *args, **kwargs):
        self.token_digest = self.digest(self.token_value)
        super(Token, self).save(*args, **kwargs)
