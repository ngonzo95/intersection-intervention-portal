# Generated by Django 4.2.4 on 2023-09-13 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("portal_app", "0004_auto_20230913_0151"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="intersection",
            name="fatal_accident_number",
        ),
        migrations.RemoveField(
            model_name="intersection",
            name="major_accident_number",
        ),
        migrations.RemoveField(
            model_name="intersection",
            name="minor_accident_number",
        ),
        migrations.RemoveField(
            model_name="intersection",
            name="property_accident_number",
        ),
        migrations.RemoveField(
            model_name="intersection",
            name="unknown_accident_number",
        ),
    ]