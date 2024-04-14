# Generated by Django 5.0.3 on 2024-04-14 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_alter_student_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='saved_courses',
            field=models.ManyToManyField(related_name='saved_students', to='base.course'),
        ),
        migrations.AlterField(
            model_name='student',
            name='enrolled_courses',
            field=models.ManyToManyField(related_name='enrolled_students', to='base.course'),
        ),
    ]