from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Board(models.Model):
    name = models.CharField(max_length=40, unique=True)
    description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Topic(models.Model):
    subject = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.DO_NOTHING)
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.DO_NOTHING)


class Post(models.Model):
    message = models.CharField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True, auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(User, null=True, related_name="+", on_delete=models.DO_NOTHING)
