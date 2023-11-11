# Generated by Django 4.2.6 on 2023-11-09 04:13

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("isbn", models.IntegerField(default=None)),
                ("author", models.CharField(default=None, max_length=200)),
                ("copies", models.IntegerField(default=0)),
                (
                    "category",
                    models.CharField(
                        blank=True, default=None, max_length=200, null=True
                    ),
                ),
                ("available", models.BooleanField(default=True)),
                ("issue_date", models.DateField(blank=True, default=None, null=True)),
                ("ret_date", models.DateField(blank=True, default=None, null=True)),
                ("issue_to", models.CharField(default=0, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Magazine",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                (
                    "category",
                    models.CharField(
                        blank=True, default=None, max_length=200, null=True
                    ),
                ),
                ("author", models.CharField(default=None, max_length=200)),
                ("isbn", models.IntegerField(default=None)),
                ("copies", models.IntegerField(default=0)),
                ("available", models.BooleanField(default=True)),
                ("issue_date", models.DateField(blank=True, default=None, null=True)),
                ("ret_date", models.DateField(blank=True, default=None, null=True)),
                ("issue_to", models.CharField(default="Do not Enter", max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Reference",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                (
                    "category",
                    models.CharField(
                        blank=True, default=None, max_length=200, null=True
                    ),
                ),
                ("author", models.CharField(default=None, max_length=200)),
                ("copies", models.IntegerField(default=0)),
                ("isbn", models.IntegerField(default=None)),
                ("available", models.BooleanField(default=True)),
                ("issue_date", models.DateField(blank=True, default=None, null=True)),
                ("ret_date", models.DateField(blank=True, default=None, null=True)),
                ("issue_to", models.CharField(default=0, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default=None, max_length=20)),
                ("usn", models.CharField(max_length=7)),
                ("phone", models.IntegerField()),
                ("email", models.CharField(max_length=50)),
                ("password", models.CharField(max_length=20)),
                ("fine", models.IntegerField(blank=True, default=0)),
                (
                    "issued_Book",
                    models.ManyToManyField(
                        blank=True, related_name="issued_by", to="website.book"
                    ),
                ),
                (
                    "issued_Reference",
                    models.ManyToManyField(
                        blank=True, related_name="issued_by", to="website.reference"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Staff",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("email", models.EmailField(max_length=200)),
                ("phone", models.IntegerField(default=0)),
                ("password", models.IntegerField()),
                ("fine", models.IntegerField(default=0)),
                ("staff_id", models.IntegerField(default=0)),
                ("issued_book", models.ManyToManyField(blank=True, to="website.book")),
                (
                    "issued_reference",
                    models.ManyToManyField(blank=True, to="website.reference"),
                ),
            ],
        ),
    ]
