# Generated by Django 4.2.6 on 2024-01-28 15:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="users",
            name="phone",
            field=models.CharField(max_length=10),
        ),
    ]
