# Generated by Django 4.0.3 on 2022-04-03 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ankiety', '0009_alter_form_close_value_alter_form_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='close_count',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
