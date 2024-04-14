# Generated by Django 5.0.3 on 2024-03-21 08:02

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weekstatus',
            name='grade',
        ),
        migrations.AddField(
            model_name='weekstatus',
            name='modified_at',
            field=models.DateField(auto_now=True),
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('created_at', models.DateField(auto_now_add=True)),
                ('week_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.weekstatus')),
            ],
        ),
    ]