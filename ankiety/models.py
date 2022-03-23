from django.db import models


class User(models.Model):
    id_user = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=40)
    created_at = models.DateTimeField()
    verified = models.BooleanField(default=False)


class Form(models.Model):
    CONDITIONS = (
        ('D', 'Date'),
        ('C', 'Users count')
    )
    id_form = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    close_condition = models.CharField(max_length=1, choices=CONDITIONS)
    close_value = models.CharField(max_length=20)
    is_close = models.BooleanField(default=False)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    items = models.JSONField()


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
