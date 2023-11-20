# Generated by Django 4.2.6 on 2023-11-18 12:39

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Users",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "user_type",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "librarian"), (2, "staff"), (3, "student")]
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("email", models.EmailField(max_length=200)),
                ("phone", models.IntegerField()),
                ("fine", models.IntegerField(default=0)),
                ("id_number", models.CharField(max_length=200)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
            ],
            options={
                "permissions": [
                    ("librarian", "Librarian"),
                    ("student", "Student"),
                    ("staff", "Staff"),
                ],
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
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
                (
                    "g",
                    models.CharField(
                        choices=[("UG", "Ug"), ("PG", "Pg")],
                        default="UG",
                        max_length=10,
                    ),
                ),
                ("edition", models.IntegerField(default=None)),
                ("author", models.CharField(default=None, max_length=200)),
                ("copies", models.IntegerField(default=0)),
                (
                    "category",
                    models.CharField(blank=True, default=None, max_length=200),
                ),
                ("issue_date", models.DateField(blank=True, default=None, null=True)),
                ("ret_date", models.DateField(blank=True, default=None, null=True)),
                (
                    "issue_to",
                    models.CharField(
                        blank=True, default=None, max_length=200, null=True
                    ),
                ),
                ("reference", models.BooleanField(default=False)),
            ],
            options={
                "permissions": [("librarian", "Librarian"), ("only_view", "Only View")],
            },
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
                    models.CharField(blank=True, default=None, max_length=200),
                ),
                ("author", models.CharField(default=None, max_length=200)),
                ("isbn", models.IntegerField(default=None)),
                ("copies", models.IntegerField(default=0)),
                ("issue_date", models.DateField(blank=True, default=None, null=True)),
                ("ret_date", models.DateField(blank=True, default=None, null=True)),
            ],
            options={
                "permissions": [("librarian", "Librarian"), ("only_view", "Only View")],
            },
        ),
        migrations.CreateModel(
            name="File",
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
                ("file", models.FileField(blank=True, null=True, upload_to="files/")),
                ("title", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "description",
                    models.CharField(blank=True, max_length=2000, null=True),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "permissions": [
                    ("librarian", "Librarian"),
                    ("staff", "Staff"),
                    ("student", "Student"),
                ],
            },
        ),
        migrations.AddField(
            model_name="users",
            name="issued_book",
            field=models.ManyToManyField(
                blank=True, related_name="users_books", to="website.book"
            ),
        ),
        migrations.AddField(
            model_name="users",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
    ]
