# Generated by Django 4.2.6 on 2023-11-02 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0005_alter_book_issue_to"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="book",
            name="issue_to",
        ),
        migrations.AlterField(
            model_name="student",
            name="issued",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="issued_by",
                to="website.book",
            ),
        ),
    ]