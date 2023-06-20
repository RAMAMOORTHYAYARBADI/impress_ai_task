from django.contrib.auth.models import User
from django.db import models

class ButtonStats(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    button = models.CharField(max_length=50)
    count = models.PositiveIntegerField(default=0)

class UserStats(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stupid_count = models.PositiveIntegerField(default=0)
    fat_count = models.PositiveIntegerField(default=0)
    dumb_count = models.PositiveIntegerField(default=0)