# Generated by Django 4.2.6 on 2024-10-28 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('resume', models.FileField(upload_to='resumes/')),
                ('primary_skills', models.JSONField()),
                ('experience', models.IntegerField()),
                ('expertise_level', models.CharField(choices=[('Beginner', 'Beginner'), ('Medium', 'Medium'), ('Expert', 'Expert')], max_length=10)),
                ('answers', models.JSONField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]