# Generated by Django 4.2.10 on 2024-03-03 13:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0002_book_volume_historicalbook_volume_message"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="book",
            name="volume",
        ),
        migrations.RemoveField(
            model_name="historicalbook",
            name="volume",
        ),
        migrations.AlterField(
            model_name="book",
            name="edition",
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="book",
            name="reference",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name="historicalbook",
            name="edition",
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="historicalbook",
            name="reference",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
