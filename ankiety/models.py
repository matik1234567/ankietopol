from django.db import models
from django.contrib.auth.models import User


class Form(models.Model):
    CONDITIONS = (
        ('N', 'No condition'),
        ('D', 'Date'),
        ('C', 'Users count')
    )
    id_form = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    close_condition = models.CharField(max_length=1, choices=CONDITIONS, default='N')
    close_value = models.CharField(max_length=30)
    is_closed = models.BooleanField(default=False)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    items = models.JSONField(default='')


class Response(models.Model):
    id_response = models.OneToOneField(
        Form,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    responses = models.JSONField()


class ChartsSettings(models.Model):
    id_settings = models.OneToOneField(
        Form,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    settings = models.JSONField()
