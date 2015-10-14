from django.db import models


class TokenQuerySet(models.QuerySet):
    def from_credential(self, token_type, token_value):
        token_digest = self.model.digest(token_value)
        return self.filter(token_type=token_type,
                           token_digest=token_digest).first()
