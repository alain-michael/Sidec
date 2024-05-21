# Generated by Django 5.0.1 on 2024-04-19 15:28

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_student_saved_courses_alter_student_enrolled_courses'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseweek',
            name='week_text',
        ),
        migrations.RemoveField(
            model_name='courseweek',
            name='week_videos',
        ),
        migrations.AddField(
            model_name='courseweek',
            name='topic',
            field=models.CharField(default='Topic', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='week',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.courseweek'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='profile_views',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)]),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='CourseMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_type', models.CharField(choices=[('text', 'Text'), ('video', 'Video')], max_length=5)),
                ('text', models.TextField(blank=True, null=True)),
                ('video', models.FileField(blank=True, null=True, upload_to='videos_uploaded', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])),
                ('week', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.courseweek')),
            ],
        ),
    ]