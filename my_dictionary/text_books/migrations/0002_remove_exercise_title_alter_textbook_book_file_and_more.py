# Generated by Django 4.1.2 on 2023-11-04 22:54

import django.core.validators
from django.db import migrations, models

import text_books.models


class Migration(migrations.Migration):
    dependencies = [
        ("text_books", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="exercise",
            name="title",
        ),
        migrations.AlterField(
            model_name="textbook",
            name="book_file",
            field=models.FileField(
                upload_to=text_books.models.TextBook.user_directory_path,
                validators=[django.core.validators.FileExtensionValidator(["pdf"])],
            ),
        ),
        migrations.AlterField(
            model_name="textbook",
            name="keys_file",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=text_books.models.TextBook.user_directory_path,
                validators=[django.core.validators.FileExtensionValidator(["pdf"])],
            ),
        ),
    ]
