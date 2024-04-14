# Generated by Django 5.0.3 on 2024-04-06 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_remove_coursecomment_user_coursecomment_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='Socials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('github', models.URLField()),
                ('instagram', models.URLField()),
                ('linkedin', models.URLField()),
                ('facebook', models.URLField()),
                ('twitter', models.URLField()),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='enrolled_courses',
            field=models.ManyToManyField(to='base.course'),
        ),
        migrations.AddField(
            model_name='student',
            name='preferred_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
