# models.py
from django.db import models

class GameMap(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.JSONField()
