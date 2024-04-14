# Generated by Django 5.0.3 on 2024-04-08 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_alter_achievement_achievement_icon_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='achievement_icon',
            field=models.ImageField(upload_to='achievement_icons'),
        ),
        migrations.AlterField(
            model_name='student',
            name='profile_pic',
            field=models.ImageField(default='https://upload.wikimedia.org/wikipedia/commons/2/2c/Default_pfp.svg', upload_to='profile_pics'),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='profile_pic',
            field=models.ImageField(default='https://upload.wikimedia.org/wikipedia/commons/2/2c/Default_pfp.svg', upload_to='profile_pics'),
        ),
    ]
