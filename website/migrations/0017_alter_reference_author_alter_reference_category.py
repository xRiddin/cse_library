# Generated by Django 4.2.6 on 2023-11-11 04:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0016_alter_return_unique_together_remove_return_book_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reference",
            name="author",
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="reference",
            name="category",
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]