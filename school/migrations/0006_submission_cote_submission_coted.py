# Generated by Django 4.0.5 on 2022-06-29 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0005_submission_date_alter_homework_notice'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='cote',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='submission',
            name='coted',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
