from django.db import models
from django.contrib.auth.models import User

class PasswordCHangeRequest(models.Model):
    account  = models.ForeignKey(User)
    req_random_key = models.CharField(max_length = 48)
    created_at = models.DateTimeField()

