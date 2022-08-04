# Generated by Django 4.0.5 on 2022-06-24 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_promotion_level_student_com_prom_submission_comment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='com_prom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='complement', to='school.promotion'),
        ),
        migrations.AlterField(
            model_name='student',
            name='matricule',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
