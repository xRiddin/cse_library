# Generated by Django 4.2.6 on 2023-11-09 12:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0005_alter_issue_reference"),
    ]

    operations = [
        migrations.AddField(
            model_name="issue",
            name="expiry_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
