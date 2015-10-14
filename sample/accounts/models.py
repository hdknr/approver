from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User)
    birth_year = models.IntegerField()
    birth_month = models.IntegerField()
    birth_day = models.IntegerField()
