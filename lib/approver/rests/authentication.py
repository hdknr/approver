from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from rest_framework import exceptions
from rest_framework.authentication import (
    BaseAuthentication, get_authorization_header)

from approver.models import Token


class BearerTokenAuthentication(BaseAuthentication):
    model = Token

    def authenticate(self, request):
        try:
            token_type, token_value = get_authorization_header(request).split()
            return self.authenticate_credentials(token_type, token_value)
        except UnicodeError:
            raise exceptions.AuthenticationFailed(
                _('Invalid token header. '
                  'Token string should not contain invalid characters.'))
        except ValueError:
            raise exceptions.AuthenticationFailed(
                _('Invalid token header. '
                  'Token string should not be blank'))

    def authenticate_credentials(self, token_type, token_value):
        try:
            token = self.model.objects.from_credential(token_type, token_value)
            return (token.user, token)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token or not token.user.is_active:
            raise exceptions.AuthenticationFailed(
                _('User inactive or deleted.'))

    def authenticate_header(self, request):
        return "Bearer"
