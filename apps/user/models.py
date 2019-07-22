from django.db import models


class User(models.Model):
    name = models.CharField(max_length=20)
    pwd = models.CharField(max_length=30)
    email = models.CharField(max_length=30)

    class Meta:
        db_table = "user"