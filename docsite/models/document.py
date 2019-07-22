from django.db import models
from docsite.models import Site


class Document(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    path = models.CharField(max_length=250, unique=True, db_index=True)
