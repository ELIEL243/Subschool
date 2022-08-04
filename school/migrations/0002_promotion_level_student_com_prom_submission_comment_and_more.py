# Generated by Django 4.0.5 on 2022-06-24 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='level',
            field=models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='com_prom',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='complement', to='school.promotion'),
        ),
        migrations.AddField(
            model_name='submission',
            name='comment',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='promotion',
            field=models.ManyToManyField(related_name='promotion', to='school.promotion'),
        ),
    ]