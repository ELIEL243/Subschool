# Generated by Django 4.0.5 on 2022-07-29 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0010_response_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
