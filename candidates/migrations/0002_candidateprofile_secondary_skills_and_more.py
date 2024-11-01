# Generated by Django 4.2.16 on 2024-10-28 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidateprofile',
            name='secondary_skills',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='candidateprofile',
            name='experience',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='candidateprofile',
            name='primary_skills',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
