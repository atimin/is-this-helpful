from django.db import models
from docsite.models import Document


class Action(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    action = models.CharField(max_length=20)
    data = models.CharField(max_length=200, null=True)


