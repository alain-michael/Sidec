# Generated by Django 5.0.1 on 2024-05-03 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_quizgrade'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizgrade',
            name='total_marks',
            field=models.IntegerField(default=8),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('MCQ', 'Multiple Choice'), ('SAN', 'Short Answer'), ('MCA', 'Multiple Correct Answers')], max_length=3),
        ),
    ]