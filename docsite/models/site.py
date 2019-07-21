from django.db import models
from django.contrib.auth.models import User


class Site(models.Model):
    domain_name = models.CharField(max_length=30, unique=True)
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE)
