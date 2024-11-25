from django.contrib.auth.models import User
from django.db import models


# Model Classes
# =============
class Ban(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reason = models.TextField(max_length=512)

    def __str__(self):
        return str(self.user)
