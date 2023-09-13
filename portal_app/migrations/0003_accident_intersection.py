# Generated by Django 4.2.4 on 2023-09-13 01:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("portal_app", "0002_create_accidents_table"),
    ]

    operations = [
        migrations.AddField(
            model_name="accident",
            name="intersection",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="portal_app.intersection",
            ),
        ),
    ]