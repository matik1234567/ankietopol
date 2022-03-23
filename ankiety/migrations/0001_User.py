# Generated by Django 4.0.3 on 2022-03-23 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id_user', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=40)),
                ('created_at', models.DateTimeField()),
                ('verified', models.BooleanField()),
            ],
        ),
    ]
