# Generated by Django 5.0.1 on 2024-05-02 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_coursematerial_time_to_complete'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='time_to_complete',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
    ]